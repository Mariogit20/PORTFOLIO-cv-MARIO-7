from django.contrib import admin
from .models import HistoriqueUser, HistoriqueRetentionSetting


@admin.register(HistoriqueRetentionSetting)
class RetentionAdmin(admin.ModelAdmin):
    list_display = ("id", "retention_years", "updated_at")


@admin.register(HistoriqueUser)
class HistoriqueUserAdmin(admin.ModelAdmin):
    list_display = ("date_action", "heure_action", "user", "action", "app_label", "model_name", "object_id")
    list_filter = ("action", "app_label", "model_name", "date_action")
    search_fields = ("user__email", "object_id", "object_repr", "url")
    ordering = ("-date_action", "-heure_action")
