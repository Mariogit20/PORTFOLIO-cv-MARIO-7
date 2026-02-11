from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User, Menu, RoleMenuAcces
from app_contact.models import Contact
from PackageUser.modul_new_user import GestionnaireUtilisateur
import re

# --- UTILITAIRES ---

# --- VUE PRINCIPALE (GESTION GLOBALE) ---

# N'oubliez pas d'importer le modèle Role en haut du fichier


from app_contact.models import Role 





def gestion_globale(request):
    """
    Page centrale : liste users + matrice permissions menus + messages contact
    - LIGNES = RÔLES
    - COLONNES = MENUS
    """
    users = User.objects.select_related("role").all()
    roles = Role.objects.all()
    menus = Menu.objects.all()
    contacts = Contact.objects.all().order_by("-date_envoi")

    # Accès existants -> format "roleId_menuId"
    acces_existants = [
        f"{a.role_id}_{a.menu_id}"
        for a in RoleMenuAcces.objects.filter(est_visible=True)
    ]

    # Menus visibles pour l'utilisateur connecté (via session)
    mes_menus_visibles = []
    user_session = request.session.get("user")
    if user_session and user_session.get("id"):
        user_obj = User.objects.filter(id=user_session["id"]).select_related("role").first()
        if user_obj and user_obj.role_id:
            mes_menus_visibles = RoleMenuAcces.objects.filter(
                role_id=user_obj.role_id,
                est_visible=True
            ).select_related("menu")

    context = {
        "users": users,
        "roles": roles,
        "menus": menus,
        "contacts": contacts,
        "acces_existants": acces_existants,
        "mes_menus_visibles": mes_menus_visibles,
    }
    return render(request, "page_utilisateur.html", context)



# --- ACTIONS SUR LES UTILISATEURS ---

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""

# app_user > views.py

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""

def add_user(request):
    """Ajoute un utilisateur via le module externe GestionnaireUtilisateur."""
    if request.method == "POST":
        gestionnaire = GestionnaireUtilisateur()
        # On traite la création (le module gère les validations et le hachage)
        return gestionnaire.creer_un_nouvel_utilisateur(request, "page_utilisateur.html")
            
    return redirect('gestion_globale')

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""

# app_user > views.py

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""


# --- GESTION DES PERMISSIONS (MENUS) ---


# https://chatgpt.com/c/698b5dc9-15bc-832f-8670-a02e56e3bcc7
def update_menus(request):
    if request.method == "POST":
        roles = Role.objects.all()
        menus = Menu.objects.all()

        for role in roles:
            for menu in menus:
                key = f"access_{role.id}_{menu.id}"
                est_coche = key in request.POST

                # ✅ Forcer Administrateur × Gestion des Utilisateurs (toujours True)
                if role.nom_role == "Administrateur" and menu.nom == "Gestion des Utilisateurs":
                    est_coche = True

                RoleMenuAcces.objects.update_or_create(
                    role=role,
                    menu=menu,
                    defaults={"est_visible": est_coche},
                )

        messages.success(request, "Permissions (par rôle) enregistrées avec succès.")
        return redirect("gestion_globale")

    return redirect("gestion_globale")


