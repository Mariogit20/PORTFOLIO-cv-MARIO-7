from django.db import models
from app_contact.models import User  # votre modèle utilisateur existant


class HistoriqueRetentionSetting(models.Model):
    """
    Singleton (1 seule ligne) : durée de conservation en années.
    Exemple : 2 => conserver année courante et année précédente.
    """
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    retention_years = models.PositiveSmallIntegerField(default=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "historique_retention_setting"

    def save(self, *args, **kwargs):
        self.pk = 1  # force singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_value(cls) -> int:
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"retention_years": 2})
        return int(obj.retention_years)


class HistoriqueUser(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Création"),
        ("READ", "Lecture"),
        ("UPDATE", "Modification"),
        ("DELETE", "Suppression"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="historiques_actions")

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    # Cible de l’action (modèle touché)
    app_label = models.CharField(max_length=80, blank=True, default="")
    model_name = models.CharField(max_length=80, blank=True, default="")
    object_id = models.CharField(max_length=64, blank=True, default="")
    object_repr = models.CharField(max_length=255, blank=True, default="")

    # DATE + HEURE (comme demandé)
    date_action = models.DateField(auto_now_add=True)
    heure_action = models.TimeField(auto_now_add=True)

    # Trace technique utile
    url = models.CharField(max_length=255, blank=True, default="")
    method = models.CharField(max_length=10, blank=True, default="")
    ip = models.CharField(max_length=64, blank=True, default="")

    details = models.TextField(blank=True, default="")

    class Meta:
        db_table = "historique_user"
        ordering = ["-date_action", "-heure_action"]
        indexes = [
            models.Index(fields=["date_action"]),
            models.Index(fields=["action"]),
            models.Index(fields=["app_label", "model_name"]),
        ]

    def __str__(self):
        return f"{self.user.email} | {self.action} | {self.app_label}.{self.model_name}#{self.object_id} | {self.date_action} {self.heure_action}"
