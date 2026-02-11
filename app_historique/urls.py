from django.urls import path
from . import views

urlpatterns = [
    path("fragment/", views.historique_fragment, name="historique_fragment"),
    path("settings/", views.historique_settings, name="historique_settings"),

    path("export/pdf/", views.export_historique_pdf, name="export_historique_pdf"),
    path("export/excel/", views.export_historique_excel, name="export_historique_excel"),
    path("export/csv/", views.export_historique_csv, name="export_historique_csv"),
]
