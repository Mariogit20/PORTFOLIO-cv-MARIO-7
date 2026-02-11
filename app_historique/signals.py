from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import HistoriqueUser
from .middleware import get_current_user

# Apps à tracer (vos apps)
TRACK_APP_LABELS = {"app_acceuil", "app_contact", "app_user"}


def _make_repr(instance) -> str:
    try:
        return str(instance)[:255]
    except Exception:
        return f"{instance.__class__.__name__}#{getattr(instance, 'pk', '')}"[:255]


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    # ignorer l’historique lui-même
    if sender._meta.app_label == "app_historique":
        return
    if sender._meta.app_label not in TRACK_APP_LABELS:
        return

    user = get_current_user()
    if not user:
        return

    HistoriqueUser.objects.create(
        user=user,
        action="CREATE" if created else "UPDATE",
        app_label=sender._meta.app_label,
        model_name=sender.__name__,
        object_id=str(getattr(instance, "pk", "") or ""),
        object_repr=_make_repr(instance),
        url="",
        method="",
        ip="",
        details=""
    )


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender._meta.app_label == "app_historique":
        return
    if sender._meta.app_label not in TRACK_APP_LABELS:
        return

    user = get_current_user()
    if not user:
        return

    HistoriqueUser.objects.create(
        user=user,
        action="DELETE",
        app_label=sender._meta.app_label,
        model_name=sender.__name__,
        object_id=str(getattr(instance, "pk", "") or ""),
        object_repr=_make_repr(instance),
        url="",
        method="",
        ip="",
        details=""
    )
