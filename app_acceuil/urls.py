# app_acceuil/urls.py
from django.urls import path
from .views import *

from app_acceuil.json_transfer import (
    export_portfolio_json,
    export_users_json,
    import_json_bundle,
)

urlpatterns = [
    # JSON transfer (ADMIN)
    path("export/portfolio/", export_portfolio_json, name="export_portfolio_json"),
    path("export/users/", export_users_json, name="export_users_json"),
    path("import/json/", import_json_bundle, name="import_json_bundle"),

    # Public
    path("", aff_acceuil_PAGE_PUBLIQUE_Vue_par_les_VISITEURS, name="name_acceuil"),
    path("index.html", aff_acceuil_PAGE_PUBLIQUE_Vue_par_les_VISITEURS, name="name_acceuil"),

    # Dashboard
    path("dashboard/", page_Mon_Espace_Administration, name="dashboard_admin"),

    # Démo live
    path("realisations/<int:realisation_id>/demo-live/", incrementer_compteur_demo_live, name="realisation_demo_live"),

    # Pages annexes
    path("Page_CAMIONS_DE_TRANSPORT_DE_MARCHANDISES/", Fonction_Page_CAMIONS_DE_TRANSPORT_DE_MARCHANDISES,
         name="name_Page_CAMIONS_DE_TRANSPORT_DE_MARCHANDISES"),
    path("Page_diapo_Javascript_Page1/", Fonction_Page_diapo_Javascript_Page1, name="name_Page_diapo_Javascript_Page1"),
    path("Page_email_Javascript/", Fonction_Page_email_Javascript, name="name_Page_email_Javascript"),

    # Ancres
    path("Page_accueil_section_Accueil/", Fonction_Page_accueil_section_Accueil, name="name_Page_accueil_section_Accueil"),
    path("Page_accueil_section_projets/", Fonction_Page_accueil_section_projets, name="name_Page_accueil_section_projets"),
    path("Page_accueil_section_temoignages/", Fonction_Page_accueil_section_temoignages, name="name_Page_accueil_section_temoignages"),
    path("Page_accueil_section_a_propos/", Fonction_Page_accueil_section_a_propos, name="name_Page_accueil_section_a_propos"),
    path("Page_accueil_section_contact/", Fonction_Page_accueil_section_contact, name="name_Page_accueil_section_contact"),

    # Reset compteur
    path("reinitialiser-compteur/<int:realisation_id>/", reinitialiser_compteur_projet, name="reinitialiser_compteur_unique"),
]
