

# # # https://gemini.google.com/app/6db35aae43a64f70
# # # https://gemini.google.com/app/6db35aae43a64f70

# # https://gemini.google.com/app/6db35aae43a64f70
# # https://gemini.google.com/app/6db35aae43a64f70
# # https://gemini.google.com/app/6db35aae43a64f70
# # https://gemini.google.com/app/6db35aae43a64f70
# # https://gemini.google.com/app/6db35aae43a64f70

# # https://gemini.google.com/app/6db35aae43a64f70
# # https://gemini.google.com/app/6db35aae43a64f70
# # https://gemini.google.com/app/6db35aae43a64f70

# # https://gemini.google.com/app/6db35aae43a64f70


# # https://gemini.google.com/app/8db05da3c2cf0a52
# # https://gemini.google.com/app/8db05da3c2cf0a52
# # https://gemini.google.com/app/8db05da3c2cf0a52
# # https://gemini.google.com/app/8db05da3c2cf0a52
# # https://gemini.google.com/app/8db05da3c2cf0a52

# # https://gemini.google.com/app/8db05da3c2cf0a52
# # https://gemini.google.com/app/8db05da3c2cf0a52



            
            
            
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# https://gemini.google.com/app/8db05da3c2cf0a52
# https://gemini.google.com/app/8db05da3c2cf0a52
# https://gemini.google.com/app/8db05da3c2cf0a52
# https://gemini.google.com/app/8db05da3c2cf0a52
# https://gemini.google.com/app/8db05da3c2cf0a52






# 2. Rappel de l'architecture globale

# Pour que tout fonctionne, votre projet doit respecter cette structure de fichiers :
# Fichier	Rôle
# models.py	Stocke les Utilisateurs, les Menus et la table de liaison MenuAcces.
# views.py	Calcule qui a droit à quoi et traite les formulaires (POST).
# urls.py	Dirige les clics sur les boutons vers les bonnes fonctions Python.
# page_utilisateur.html	Affiche la Navbar dynamique et la Matrice de cases à cocher.
# admin_extras.py	(Filtre) Permet au template de lire le dictionnaire des accès.

from app_contact.models import User, Role


class Menu(models.Model):
    nom = models.CharField(max_length=100)
    code_menu = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom



class RoleMenuAcces(models.Model):
    """
    (Nouveau système) Accès par rôle : LIGNES = rôles, COLONNES = menus.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    est_visible = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'menu')

    def __str__(self):
        return f"{self.role.nom_role} -> {self.menu.nom} ({'visible' if self.est_visible else 'caché'})"


# ---------------------------------------------------------------------
# INITIALISATIONS AUTOMATIQUES (pratique pour éviter les "trous")
# ---------------------------------------------------------------------
@receiver(post_save, sender=Role)
def creer_permissions_pour_nouveau_role(sender, instance, created, **kwargs):
    if not created:
        return

    menus = Menu.objects.all()
    for menu in menus:
        default_visible = (
            instance.nom_role == "Administrateur"
            and menu.nom == "Gestion des Utilisateurs"
        )
        RoleMenuAcces.objects.get_or_create(
            role=instance,
            menu=menu,
            defaults={"est_visible": default_visible},
        )



@receiver(post_save, sender=Menu)
def creer_permissions_pour_nouveau_menu(sender, instance, created, **kwargs):
    if not created:
        return

    roles = Role.objects.all()
    for role in roles:
        default_visible = (
            role.nom_role == "Administrateur"
            and instance.nom == "Gestion des Utilisateurs"
        )
        RoleMenuAcces.objects.get_or_create(
            role=role,
            menu=instance,
            defaults={"est_visible": default_visible},
        )


