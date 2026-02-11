from django.contrib import admin
from .models import (
    Projetscards, Projetsfirstspeciality, Projetmesrealisations, 
    Projetphotodeprofil, ProjetAproposDeMoi, MesCompetencesCles, ReseauSocial
)



# https://gemini.google.com/app/b83bdb7ebec35a6c
# https://gemini.google.com/app/b83bdb7ebec35a6c
# https://gemini.google.com/app/b83bdb7ebec35a6c
# https://gemini.google.com/app/b83bdb7ebec35a6c
# https://gemini.google.com/app/b83bdb7ebec35a6c


# 1. Cartes de témoignages
class DashProjetsCards(admin.ModelAdmin):
    list_display = ("nom", "images", "est_visible", "created_at")
    list_editable = ("est_visible",) # Permet de cocher/décocher sans ouvrir la fiche

# 2. Spécialité (Singleton : une seule ligne autorisée)
class DashProjetsFirstSpeciality(admin.ModelAdmin):
    list_display = ("description_speciality", "est_visible")
    list_editable = ("est_visible",)
        
    def has_add_permission(self, request):
        if Projetsfirstspeciality.objects.exists():
            return False
        return True

# 3. Réalisations
class DashProjetsMesRealisations(admin.ModelAdmin):
    list_display = ("nom", "images", "est_visible", "created_at")
    list_editable = ("est_visible",)

# 4. Photo de Profil (Singleton)
class DashProjetPhotoDeProfil(admin.ModelAdmin):
    list_display = ("images", "est_visible")
    list_editable = ("est_visible",)
        
    def has_add_permission(self, request):
        if Projetphotodeprofil.objects.exists():
            return False
        return True

# 5. À propos de moi (Singleton)
class DashProjetAproposDeMoi(admin.ModelAdmin):
    list_display = ("description", "est_visible")
    list_editable = ("est_visible",)
        
    def has_add_permission(self, request):
        if ProjetAproposDeMoi.objects.exists():
            return False
        return True

# 6. Compétences Clés (Déjà enregistré via décorateur @admin.register)
@admin.register(MesCompetencesCles)
class CompetenceCleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'est_visible', 'created_at')
    list_editable = ('est_visible',)
    search_fields = ('nom',)
    list_filter = ('est_visible', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(ReseauSocial)
class ReseauSocialAdmin(admin.ModelAdmin):
    list_display = ('nom', 'url', 'est_visible')

# --- Enregistrement des modèles ---
modeles = {
    Projetscards: DashProjetsCards,
    Projetsfirstspeciality: DashProjetsFirstSpeciality,
    Projetmesrealisations: DashProjetsMesRealisations,
    Projetphotodeprofil: DashProjetPhotoDeProfil,
    ProjetAproposDeMoi: DashProjetAproposDeMoi
    
}

for model, dash in modeles.items():
    admin.site.register(model, dash)