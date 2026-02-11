import base64
import hashlib
import json
import mimetypes
import re
from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID

from django.apps import apps
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models import ForeignKey
from django.db.models.fields.files import FileField, ImageField
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect


# ----------------------------
# Helpers : sécurité + JSON
# ----------------------------
def _is_admin_session(request) -> bool:
    """
    Basé sur ta logique de session :
    request.session['user'] = { id, nom, role, ... }
    """
    user_data = request.session.get("user")
    return bool(user_data and user_data.get("role") == "Administrateur")


def _json_compatible_value(value):
    """Rend une valeur sérialisable JSON."""
    if value is None:
        return None

    if isinstance(value, (datetime, date, time)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, UUID):
        return str(value)

    return value


def _safe_json_response(payload: dict, filename: str) -> HttpResponse:
    """Construit une réponse HTTP de téléchargement JSON."""
    content = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
    resp = HttpResponse(content, content_type="application/json; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


# ----------------------------
# Normalisation + fingerprint
# ----------------------------
def _norm_text(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    return s.lower()


def _norm_email(s: str) -> str:
    return _norm_text(s)


def _fingerprint_projetscards(nom: str, description: str) -> str:
    base = f"{_norm_text(nom)}||{_norm_text(description)}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


# ----------------------------
# Serialize : Django -> dict
# ----------------------------
def _serialize_instance(obj):
    """
    Convertit un objet Django en dict JSON-friendly.
    - Champs simples => _json_compatible_value
    - Image/File => base64 + meta
    - ForeignKey => export en *_id (int) + champ logique (compat)
    """
    data = {"__model__": f"{obj._meta.app_label}.{obj.__class__.__name__}", "id": obj.pk}

    for field in obj._meta.fields:
        name = field.name
        if name == "id":
            continue

        value = getattr(obj, name)

        # Fichiers / images
        if isinstance(field, (FileField, ImageField)):
            if value and getattr(value, "name", None):
                file_path = value.name
                b64 = None
                try:
                    with default_storage.open(file_path, "rb") as f:
                        raw = f.read()
                    b64 = base64.b64encode(raw).decode("utf-8")
                except Exception:
                    b64 = None

                mime, _ = mimetypes.guess_type(file_path)
                data[name] = {
                    "storage_path": file_path,
                    "filename": file_path.split("/")[-1],
                    "mimetype": mime or "application/octet-stream",
                    "base64": b64,
                }
            else:
                data[name] = None
            continue

        # ForeignKey: stocker un entier (id) pour réimport fiable
        if isinstance(field, ForeignKey):
            # on exporte le champ logique en id (compatibilité)
            data[name] = getattr(obj, f"{name}_id")
            continue

        data[name] = _json_compatible_value(value)

    return data


def _serialize_queryset(qs):
    return [_serialize_instance(o) for o in qs]


# ----------------------------
# EXPORTS
# ----------------------------
def export_portfolio_json(request):
    if not _is_admin_session(request):
        return HttpResponseForbidden("Accès refusé (Admin uniquement).")

    from app_acceuil.models import (
        MesCompetencesCles,
        ProjetAproposDeMoi,
        Projetmesrealisations,
        Projetphotodeprofil,
        Projetscards,
        Projetsfirstspeciality,
        ReseauSocial,
    )

    payload = {
        "export_type": "portfolio",
        "exported_at": datetime.now().isoformat(),
        "version": 2,
        "data": {
            "app_acceuil.Projetphotodeprofil": _serialize_queryset(Projetphotodeprofil.objects.all()),
            "app_acceuil.ProjetAproposDeMoi": _serialize_queryset(ProjetAproposDeMoi.objects.all()),
            "app_acceuil.Projetsfirstspeciality": _serialize_queryset(Projetsfirstspeciality.objects.all()),
            "app_acceuil.Projetmesrealisations": _serialize_queryset(Projetmesrealisations.objects.all()),
            "app_acceuil.Projetscards": _serialize_queryset(Projetscards.objects.all()),
            "app_acceuil.MesCompetencesCles": _serialize_queryset(MesCompetencesCles.objects.all()),
            "app_acceuil.ReseauSocial": _serialize_queryset(ReseauSocial.objects.all()),
        },
    }

    date_prefix = datetime.now().strftime("%Y%m%d")
    return _safe_json_response(payload, f"{date_prefix}_export_portfolio.json")


def export_users_json(request):
    if not _is_admin_session(request):
        return HttpResponseForbidden("Accès refusé (Admin uniquement).")

    from app_contact.models import Contact, Role, User
    from app_user.models import Menu, RoleMenuAcces

    payload = {
        "export_type": "users",
        "exported_at": datetime.now().isoformat(),
        "version": 2,
        "notes": [
            "User.password est exporté tel quel (hash).",
            "Les ForeignKey sont exportées en identifiants (ex: role=1).",
        ],
        "data": {
            "app_contact.Role": _serialize_queryset(Role.objects.all()),
            "app_contact.User": _serialize_queryset(User.objects.all()),
            "app_contact.Contact": _serialize_queryset(Contact.objects.all()),
            "app_user.Menu": _serialize_queryset(Menu.objects.all()),
            "app_user.RoleMenuAcces": _serialize_queryset(RoleMenuAcces.objects.all()),
        },
    }

    date_prefix = datetime.now().strftime("%Y%m%d")
    return _safe_json_response(payload, f"{date_prefix}_export_users.json")


# ----------------------------
# IMPORTS
# ----------------------------
def _parse_uploaded_json(uploaded_file):
    raw = uploaded_file.read()
    try:
        text = raw.decode("utf-8")
    except Exception:
        text = raw.decode("latin-1")
    return json.loads(text)


def _restore_file_field(model_instance, field_name: str, file_dict: dict):
    """
    file_dict = {filename, base64, mimetype, storage_path, ...}
    => écrit via ImageField/FileField.save()
    """
    if not file_dict:
        return

    b64 = file_dict.get("base64")
    filename = file_dict.get("filename") or "file.bin"
    if not b64:
        return

    try:
        raw = base64.b64decode(b64)
    except Exception:
        return

    django_file = ContentFile(raw, name=filename)
    field = getattr(model_instance, field_name)
    field.save(filename, django_file, save=False)


# -------------------------------------------------
# FUSION INTELLIGENTE : clés métier
# -------------------------------------------------
SMART_MATCH_KEYS = {
    # Portfolio
    "app_acceuil.MesCompetencesCles": ["nom"],
    "app_acceuil.ReseauSocial": ["nom"],
    "app_acceuil.Projetmesrealisations": ["nom"],

    # Témoignages: match dur par fingerprint
    "app_acceuil.Projetscards": ["fingerprint"],

    # Users
    "app_contact.Role": ["nom_role"],
    "app_contact.User": ["email"],
    "app_user.Menu": ["code_menu"],
    "app_user.RoleMenuAcces": ["role", "menu"],
}


def _get_instance_by_smart_keys(Model, model_label: str, fields_data: dict):
    keys = SMART_MATCH_KEYS.get(model_label)
    if not keys:
        return None

    lookup = {}
    for k in keys:
        if k not in fields_data:
            return None
        v = fields_data[k]
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        lookup[k] = v

    try:
        return Model.objects.filter(**lookup).first()
    except Exception:
        return None


def _assign_field(instance, field, value):
    """
    Affectation robuste :
    - File/Image => gérés ailleurs
    - ForeignKey : accepter int/str-int (id) et assigner sur <name>_id
    """
    name = field.name

    if isinstance(field, ForeignKey):
        if value is None or value == "":
            setattr(instance, f"{name}_id", None)
            return

        # Si on reçoit déjà un int => OK
        if isinstance(value, int):
            setattr(instance, f"{name}_id", value)
            return

        # str -> int si possible
        if isinstance(value, str):
            s = value.strip()
            if s.isdigit():
                setattr(instance, f"{name}_id", int(s))
                return

        # dict -> récupérer id si présent
        if isinstance(value, dict) and "id" in value:
            try:
                setattr(instance, f"{name}_id", int(value["id"]))
                return
            except Exception:
                pass

        # fallback : si on reçoit un objet Role/Menu etc, essayer pk
        if hasattr(value, "pk"):
            setattr(instance, f"{name}_id", value.pk)
            return

        # sinon on laisse Django lever proprement
        setattr(instance, name, value)
        return

    setattr(instance, name, value)


def _upsert_objects(model_label: str, objects_list: list, keep_ids: bool = True, exclude_fields: set | None = None):
    """
    UPSERT intelligent (sans suppression) :
    1) Si id existe en base -> update
    2) Sinon -> tentative match via SMART_MATCH_KEYS
    3) Sinon -> create
    """
    Model = apps.get_model(model_label)
    exclude_fields = exclude_fields or set()

    for obj_data in objects_list:
        obj_id = obj_data.get("id")

        fields_data = {
            k: v for k, v in obj_data.items()
            if k not in {"__model__", "id"} and k not in exclude_fields
        }

        # séparer file fields
        file_payloads = {}
        for field in Model._meta.fields:
            if isinstance(field, (FileField, ImageField)) and field.name in fields_data:
                file_payloads[field.name] = fields_data.pop(field.name)

        # Projetscards : calc fingerprint si absent
        if model_label == "app_acceuil.Projetscards":
            if not fields_data.get("fingerprint"):
                fields_data["fingerprint"] = _fingerprint_projetscards(
                    fields_data.get("nom", ""),
                    fields_data.get("description", ""),
                )

        instance = None

        # 1) update par ID si existant
        if keep_ids and obj_id is not None:
            instance = Model.objects.filter(pk=obj_id).first()

        # 2) update par clé métier
        if instance is None:
            instance = _get_instance_by_smart_keys(Model, model_label, fields_data)

        # 3) create
        if instance is None:
            instance = Model(pk=obj_id) if (keep_ids and obj_id is not None) else Model()

        # appliquer champs + normalisation à l’enregistrement
        for field in Model._meta.fields:
            k = field.name
            if k == "id" or k not in fields_data:
                continue

            v = fields_data[k]

            # normalisations sûres (anti-doublons)
            if model_label == "app_contact.User" and k == "email" and isinstance(v, str):
                v = _norm_email(v)

            if model_label == "app_contact.Role" and k == "nom_role" and isinstance(v, str):
                v = _norm_text(v)

            if model_label == "app_user.Menu" and k == "code_menu" and isinstance(v, str):
                v = _norm_text(v)

            if model_label == "app_acceuil.MesCompetencesCles" and k == "nom" and isinstance(v, str):
                v = _norm_text(v)

            if model_label == "app_acceuil.ReseauSocial" and k == "nom" and isinstance(v, str):
                v = _norm_text(v)

            if model_label == "app_acceuil.Projetscards" and k == "fingerprint" and isinstance(v, str):
                v = v.strip().lower()

            if model_label == "app_acceuil.Projetscards" and k in ("nom", "description") and isinstance(v, str):
                v = v.strip()

            _assign_field(instance, field, v)

        # restaurer fichiers
        for field_name, payload in file_payloads.items():
            _restore_file_field(instance, field_name, payload)

        instance.save()


@transaction.atomic
def import_json_bundle(request):
    """
    POST depuis page_administration.html
    Inputs:
    - json_portfolio (optionnel)
    - json_users (optionnel)
    - replace_portfolio (checkbox)
    - replace_users (checkbox)

    Sans synchroniser :
    - si replace_* est coché : purge + import
    - sinon : upsert intelligent + AUCUNE suppression
    """
    if not _is_admin_session(request):
        return HttpResponseForbidden("Accès refusé (Admin uniquement).")

    if request.method != "POST":
        return redirect("dashboard_admin")

    json_portfolio = request.FILES.get("json_portfolio")
    json_users = request.FILES.get("json_users")
    replace_portfolio = bool(request.POST.get("replace_portfolio"))
    replace_users = bool(request.POST.get("replace_users"))

    # -------- Portfolio import --------
    if json_portfolio:
        try:
            data = _parse_uploaded_json(json_portfolio)
            if data.get("export_type") != "portfolio":
                raise ValueError("Ce fichier n'est pas un export portfolio.")
            model_map = data.get("data", {})
            if not isinstance(model_map, dict):
                raise ValueError("Format JSON invalide: data doit être un objet (dict).")

            if replace_portfolio:
                from app_acceuil.models import (
                    MesCompetencesCles,
                    ProjetAproposDeMoi,
                    Projetmesrealisations,
                    Projetphotodeprofil,
                    Projetscards,
                    Projetsfirstspeciality,
                    ReseauSocial,
                )
                ReseauSocial.objects.all().delete()
                MesCompetencesCles.objects.all().delete()
                Projetscards.objects.all().delete()
                Projetmesrealisations.objects.all().delete()
                Projetsfirstspeciality.objects.all().delete()
                ProjetAproposDeMoi.objects.all().delete()
                Projetphotodeprofil.objects.all().delete()

            for model_label, objects_list in model_map.items():
                _upsert_objects(model_label, objects_list, keep_ids=True)

            messages.success(request, "Import Portfolio terminé avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur import portfolio: {e}")

    # -------- Users import --------
    if json_users:
        try:
            data = _parse_uploaded_json(json_users)
            if data.get("export_type") != "users":
                raise ValueError("Ce fichier n'est pas un export users.")
            model_map = data.get("data", {})
            if not isinstance(model_map, dict):
                raise ValueError("Format JSON invalide: data doit être un objet (dict).")

            if replace_users:
                from app_user.models import Menu, RoleMenuAcces
                from app_contact.models import Contact, Role, User

                RoleMenuAcces.objects.all().delete()
                Contact.objects.all().delete()
                User.objects.all().delete()
                Menu.objects.all().delete()
                Role.objects.all().delete()

            ordered = [
                "app_contact.Role",
                "app_user.Menu",
                "app_contact.User",
                "app_contact.Contact",
                "app_user.RoleMenuAcces",
            ]
            for model_label in ordered:
                if model_label in model_map:
                    _upsert_objects(model_label, model_map[model_label], keep_ids=True)

            messages.success(request, "Import Utilisateurs terminé avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur import utilisateurs: {e}")

    return redirect("dashboard_admin")
