from datetime import date
from django.utils import timezone
from .models import HistoriqueUser, HistoriqueRetentionSetting


def purge_old_history() -> int:
    """
    Conserve N années : année courante + (N-1) années précédentes.
    Ex: année=2026, N=2 => conserve 2026 et 2025 ; supprime <= 2024.
    """
    retention_years = HistoriqueRetentionSetting.get_value()
    current_year = timezone.now().year

    threshold_year = current_year - retention_years + 1  # ex 2026-2+1 = 2025
    threshold_date = date(threshold_year, 1, 1)

    qs = HistoriqueUser.objects.filter(date_action__lt=threshold_date)
    deleted_count = qs.count()
    qs.delete()
    return deleted_count
