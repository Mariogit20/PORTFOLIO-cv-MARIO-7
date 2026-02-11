from django.apps import AppConfig


class AppHistoriqueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_historique"

    def ready(self):
        # Active les signaux (CREATE/UPDATE/DELETE)
        from . import signals  # noqa: F401
