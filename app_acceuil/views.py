from django.contrib import messages
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    MesCompetencesCles,
    ProjetAproposDeMoi,
    Projetmesrealisations,
    Projetphotodeprofil,
    Projetscards,
    Projetsfirstspeciality,
    ReseauSocial,
)

from app_contact.models import User as ContactUser
from app_user.models import RoleMenuAcces


def _get_role_id_from_session(request):
    """
    Retourne role_id de l'utilisateur connecté via request.session['user']['id'].
    Sinon None.
    """
    user_session = request.session.get("user")
    if not user_session:
        return None

    user_id = user_session.get("id")
    if not user_id:
        return None

    u = ContactUser.objects.filter(id=user_id).select_related("role").first()
    if not u:
        return None

    return u.role_id


# =========================================================================
# 1) PAGE PUBLIQUE (portfolio)
# =========================================================================
def aff_acceuil_PAGE_PUBLIQUE_Vue_par_les_VISITEURS(request):
    """Filtre et affiche uniquement les éléments marqués comme visibles."""
    temoignages = Projetscards.objects.filter(est_visible=True)
    specialites = Projetsfirstspeciality.objects.filter(est_visible=True)
    realisations = Projetmesrealisations.objects.filter(est_visible=True)
    mescompetencescles = MesCompetencesCles.objects.filter(est_visible=True)
    reseaux = ReseauSocial.objects.filter(est_visible=True)

    photodeprofil = Projetphotodeprofil.objects.filter(est_visible=True).first()
    aproposdemoi = ProjetAproposDeMoi.objects.filter(est_visible=True).first()

    # Menus visibles (par rôle)
    mes_menus_visibles = []
    role_id = _get_role_id_from_session(request)
    if role_id:
        mes_menus_visibles = (
            RoleMenuAcces.objects.filter(role_id=role_id, est_visible=True)
            .select_related("menu")
        )

    contenu = {
        "TEMOIGNAGES_des_PERSONNES_cards": temoignages,
        "EXISTENCE_de_TEMOIGNAGES": temoignages.exists(),
        "AFFICHER_la_PREMIERE_SPECIAISATION": specialites,
        "EXISTENCE_de_PREMIERE_SPECIAISATION": specialites.exists(),
        "AFFICHER_les_REALISATIONS_PERSONNELLES": realisations,
        "EXISTENCE_de_REALISATIONS_PERSONNELLES": realisations.exists(),
        "AFFICHER_la_PHOTO_DE_PROFIL": photodeprofil,
        "A_PROPOS_DE_MOI": aproposdemoi,
        "Mes_Competences_Cles": mescompetencescles,
        "Mes_Reseaux": reseaux,
        "mes_menus_visibles": mes_menus_visibles,
    }
    return render(request, "index.html", contenu)


# =========================================================================
# 2) DASHBOARD ADMINISTRATION
# =========================================================================
def page_Mon_Espace_Administration(request):
    # Accès : Administrateur ou Modérateur
    user_data = request.session.get("user")
    if not user_data or (user_data.get("role") not in {"Administrateur", "Moderateur"}):
        messages.error(request, "Accès refusé : vous devez être Administrateur ou Modérateur.")
        return redirect("name_acceuil")

    # Données existantes
    photo_profil = Projetphotodeprofil.objects.first()
    a_propos = ProjetAproposDeMoi.objects.first()
    specialite = Projetsfirstspeciality.objects.first()

    if request.method == "POST":

        # --- PHOTO DE PROFIL (SWITCH AUTO) ---
        if "btn_visibilite_photo_auto" in request.POST:
            vis = "est_visible" in request.POST
            if photo_profil:
                photo_profil.est_visible = vis
                photo_profil.save()
            messages.info(request, "Visibilité de la photo mise à jour.")

        # --- PHOTO DE PROFIL (UPLOAD/UPDATE) ---
        elif "btn_photo" in request.POST:
            img = request.FILES.get("images")
            if photo_profil:
                if img:
                    photo_profil.images = img
                photo_profil.save()
            else:
                Projetphotodeprofil.objects.create(images=img, est_visible=True)
            messages.success(request, "Photo enregistrée.")

        elif "btn_supprimer_photo" in request.POST:
            if photo_profil:
                photo_profil.delete()
            messages.warning(request, "Photo supprimée.")

        # --- À PROPOS (BIO - SWITCH AUTO) ---
        elif "btn_visibilite_bio_auto" in request.POST:
            vis = "est_visible_bio" in request.POST
            if a_propos:
                a_propos.est_visible = vis
                a_propos.save()
            messages.info(request, "Visibilité de la bio mise à jour.")

        # --- À PROPOS (BIO - TEXTE) ---
        elif "btn_apropos" in request.POST:
            description = request.POST.get("description") or ""
            if a_propos:
                a_propos.description = description
                a_propos.save()
            else:
                ProjetAproposDeMoi.objects.create(description=description, est_visible=True)
            messages.success(request, "Texte de la bio mis à jour.")

        elif "btn_supprimer_apropos" in request.POST:
            if a_propos:
                a_propos.delete()
            messages.error(request, "Texte biographique supprimé.")

        # --- SPÉCIALITÉ ---
        elif "btn_visibilite_section_spec" in request.POST:
            vis = "est_visible" in request.POST
            Projetsfirstspeciality.objects.all().update(est_visible=vis)
            messages.info(request, "Visibilité section Spécialité modifiée.")

        elif "btn_specialite" in request.POST:
            img = request.FILES.get("images")
            desc = request.POST.get("description_speciality") or ""
            if specialite:
                specialite.description_speciality = desc
                if img:
                    specialite.images = img
                specialite.save()
            else:
                Projetsfirstspeciality.objects.create(
                    description_speciality=desc, images=img, est_visible=True
                )
            messages.success(request, "Détails de la spécialité mis à jour.")

        # --- RÉALISATIONS (PROJETS) ---
        elif "btn_visibilite_section_real" in request.POST:
            vis = "est_visible" in request.POST
            Projetmesrealisations.objects.all().update(est_visible=vis)
            messages.info(request, "Section Projets mise à jour.")

        elif "btn_bascule_vis_real" in request.POST:
            obj = get_object_or_404(Projetmesrealisations, id=request.POST.get("id_realisation"))
            obj.est_visible = not obj.est_visible
            obj.save()

        elif "btn_ajouter_real" in request.POST:
            Projetmesrealisations.objects.create(
                nom=request.POST.get("nom"),
                description=request.POST.get("description"),
                images=request.FILES.get("images"),
                est_visible=True,
            )
            messages.success(request, "Projet ajouté.")

        elif "btn_modifier_real" in request.POST:
            obj = get_object_or_404(Projetmesrealisations, id=request.POST.get("id_realisation"))
            obj.nom = request.POST.get("nom")
            obj.description = request.POST.get("description")
            if request.FILES.get("images"):
                obj.images = request.FILES.get("images")
            obj.save()
            messages.info(request, "Projet modifié.")

        elif "btn_supprimer_real" in request.POST:
            get_object_or_404(Projetmesrealisations, id=request.POST.get("id_realisation")).delete()
            messages.warning(request, "Projet supprimé.")

        # --- TÉMOIGNAGES ---
        elif "btn_visibilite_section_tem" in request.POST:
            vis = "est_visible" in request.POST
            Projetscards.objects.all().update(est_visible=vis)

        elif "btn_bascule_vis_tem" in request.POST:
            obj = get_object_or_404(Projetscards, id=request.POST.get("id_temoignage"))
            obj.est_visible = not obj.est_visible
            obj.save()

        elif "btn_ajouter_temoignage" in request.POST:
            nom = (request.POST.get("nom") or "").strip()
            description = (request.POST.get("description") or "").strip()
            img = request.FILES.get("images")

            # ✅ clé stable anti-doublon (évite IntegrityError + ValidationError fingerprint unique)
            fp = Projetscards.make_fingerprint(nom, description)

            # on "upsert" le témoignage sur fingerprint
            obj, created = Projetscards.objects.update_or_create(
                fingerprint=fp,
                defaults={
                    "nom": nom,
                    "description": description,
                    "est_visible": True,
                    # images: uniquement si upload présent (sinon on conserve l'existante)
                    **({"images": img} if img else {}),
                },
            )

            messages.success(
                request,
                "Témoignage ajouté." if created else "Témoignage déjà existant : mis à jour.",
            )

        elif "btn_modifier_temoignage" in request.POST:
            obj = get_object_or_404(Projetscards, id=request.POST.get("id_temoignage"))
            obj.nom = (request.POST.get("nom") or "").strip()
            obj.description = (request.POST.get("description") or "").strip()
            if request.FILES.get("images"):
                obj.images = request.FILES.get("images")
            # fingerprint recalculé automatiquement par save()
            obj.save()
            messages.info(request, "Témoignage modifié.")

        elif "btn_supprimer_temoignage" in request.POST:
            get_object_or_404(Projetscards, id=request.POST.get("id_temoignage")).delete()
            messages.warning(request, "Témoignage supprimé.")

        # --- COMPÉTENCES ---
        elif "btn_visibilite_section_comp" in request.POST:
            vis = "est_visible" in request.POST
            MesCompetencesCles.objects.all().update(est_visible=vis)

        elif "btn_bascule_vis_comp" in request.POST:
            obj = get_object_or_404(MesCompetencesCles, id=request.POST.get("id_competence"))
            obj.est_visible = not obj.est_visible
            obj.save()

        elif "btn_ajouter_comp" in request.POST:
            MesCompetencesCles.objects.create(
                nom=request.POST.get("nom_competence"),
                est_visible=True,
            )
            messages.success(request, "Compétence ajoutée.")

        elif "btn_supprimer_comp" in request.POST:
            get_object_or_404(MesCompetencesCles, id=request.POST.get("id_competence")).delete()

        # --- RÉSEAUX SOCIAUX ---
        elif "btn_visibilite_section_res" in request.POST:
            vis = "est_visible" in request.POST
            ReseauSocial.objects.all().update(est_visible=vis)

        elif "btn_reseau" in request.POST:
            nom = (request.POST.get("nom_reseau") or "").strip()
            url = (request.POST.get("url_reseau") or "").strip()

            # Normalisations simples
            if nom.lower() == "email" and url.lower().startswith("mailto:"):
                url = url.split(":", 1)[1].strip()
            if nom.lower() == "whatsapp" and url and url.startswith("wa.me/"):
                url = "https://" + url

            ReseauSocial.objects.update_or_create(
                nom=nom,
                defaults={"url": url, "est_visible": True},
            )
            messages.success(request, "Réseau mis à jour.")

        elif "btn_supprimer_reseau" in request.POST:
            get_object_or_404(ReseauSocial, id=request.POST.get("id_reseau")).delete()

        return redirect("dashboard_admin")

    context = {
        "AFFICHER_la_PHOTO_DE_PROFIL": photo_profil,
        "A_PROPOS_DE_MOI": a_propos,
        "SPECIALITE": specialite,
        "AFFICHER_les_REALISATIONS_PERSONNELLES": Projetmesrealisations.objects.all().order_by("-id"),
        "REALISATIONS_STATS": Projetmesrealisations.objects.all().order_by("-compteur_demo_live", "-id"),
        "TOTAL_CLICS_DEMO_LIVE": (Projetmesrealisations.objects.aggregate(total=Sum("compteur_demo_live"))["total"] or 0),
        "TEMOIGNAGES_des_PERSONNES_cards": Projetscards.objects.all().order_by("-id"),
        "Mes_Competences_Cles": MesCompetencesCles.objects.all().order_by("nom"),
        "Mes_Reseaux": ReseauSocial.objects.all(),
    }
    return render(request, "page_administration.html", context)


# =========================================================================
# 2bis) COMPTEUR DE CLICS "DÉMO LIVE"
# =========================================================================
def incrementer_compteur_demo_live(request, realisation_id):
    """Incrémente le compteur quand un visiteur clique sur 'Démo Live' puis redirige vers la démo."""
    Projetmesrealisations.objects.filter(id=realisation_id).update(
        compteur_demo_live=F("compteur_demo_live") + 1
    )
    return redirect("name_Page_CAMIONS_DE_TRANSPORT_DE_MARCHANDISES")


# =========================================================================
# 3) REDIRECTIONS
# =========================================================================
def Fonction_Page_accueil_section_Accueil(request):
    return redirect("/#accueil")


def Fonction_Page_accueil_section_projets(request):
    return redirect("/#projets")


def Fonction_Page_accueil_section_temoignages(request):
    return redirect("/#temoignages")


def Fonction_Page_accueil_section_a_propos(request):
    return redirect("/#a-propos")


def Fonction_Page_accueil_section_contact(request):
    return redirect("/#contact")


def Fonction_Page_email_Javascript(request):
    return render(request, "email_Javascript.htm")


def Fonction_Page_CAMIONS_DE_TRANSPORT_DE_MARCHANDISES(request):
    return render(request, "TransportRoutier_Main.html")


def Fonction_Page_diapo_Javascript_Page1(request):
    return render(request, "diapo_Javascript_Page1.html")


# =========================================================================
# RÉINITIALISATION DU COMPTEUR POUR UN PROJET SPÉCIFIQUE
# =========================================================================
def reinitialiser_compteur_projet(request, realisation_id):
    """Remet à zéro le compteur de clics pour un projet donné."""
    projet = get_object_or_404(Projetmesrealisations, id=realisation_id)
    projet.compteur_demo_live = 0
    projet.save()
    messages.warning(request, f"Le compteur pour '{projet.nom}' a été réinitialisé.")
    return redirect("dashboard_admin")
