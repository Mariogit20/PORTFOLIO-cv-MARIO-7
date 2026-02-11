from django.core.management.base import BaseCommand
from app_historique.services import purge_old_history

class Command(BaseCommand):
    help = "Purge l'historique utilisateur selon la durée configurée."

    def handle(self, *args, **options):
        deleted = purge_old_history()
        self.stdout.write(self.style.SUCCESS(f"Purge terminée: {deleted} lignes supprimées."))
