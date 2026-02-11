from django.db import models
import re
import hashlib


def nettoyer_espaces(chaine):
    """Supprime les espaces multiples et trims."""
    if chaine:
        return " ".join(str(chaine).split())
    return chaine


# 1. TEMOIGNAGES
class Projetscards(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=False)
    # ✅ blank=True : évite ValidationError si tu fais une mise à jour sans renvoyer l'image
    images = models.ImageField(upload_to="static/images/", null=True, blank=True)
    description = models.TextField(null=True, blank=False)

    # Anti-doublon stable (tolérant aux espaces/majuscules)
    fingerprint = models.CharField(max_length=64, unique=True, db_index=True, blank=True, default="")

    est_visible = models.BooleanField(default=True, verbose_name="Afficher sur le site")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages Clients"
        ordering = ["-created_at"]

    @staticmethod
    def _norm_text(s: str) -> str:
        s = (s or "").strip()
        s = re.sub(r"\s+", " ", s)
        return s.lower()

    @classmethod
    def make_fingerprint(cls, nom: str, description: str) -> str:
        base = f"{cls._norm_text(nom)}||{cls._norm_text(description)}"
        return hashlib.sha256(base.encode("utf-8")).hexdigest()

    def clean(self):
        self.nom = nettoyer_espaces(self.nom)
        # on ne touche pas description (contenu visible)

    def save(self, *args, **kwargs):
        # Génère/normalise le fingerprint avant validation
        if not self.fingerprint:
            self.fingerprint = self.make_fingerprint(self.nom or "", self.description or "")
        self.fingerprint = (self.fingerprint or "").strip().lower()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom if self.nom else f"Témoignage {self.id}"


# 2. SPECIALITES
class Projetsfirstspeciality(models.Model):
    images = models.ImageField(upload_to="static/images/", null=True, blank=True)
    description_speciality = models.TextField(null=True, blank=False)
    est_visible = models.BooleanField(default=True, verbose_name="Afficher sur le site")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Ma Photo de Spécialisation"
        verbose_name_plural = "Mes Photos de Spécialisation"
        ordering = ["-created_at"]

    def __str__(self):
        return self.description_speciality[:50] if self.description_speciality else f"Spécialité {self.id}"


# 3. REALISATIONS
class Projetmesrealisations(models.Model):
    # NB: ton import json_transfer utilise "nom_projet" dans SMART_MATCH_KEYS.
    # Si ton champ s'appelle "nom", change SMART_MATCH_KEYS en conséquence (ou inversement).
    nom = models.CharField(max_length=100, null=True, blank=False)
    images = models.ImageField(upload_to="static/images/", null=True, blank=True)
    description = models.TextField(null=True, blank=False)
    est_visible = models.BooleanField(default=True, verbose_name="Afficher sur le site")
    compteur_demo_live = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Mes Projets"
        ordering = ["-created_at"]

    def clean(self):
        self.nom = nettoyer_espaces(self.nom)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom if self.nom else f"Projet {self.id}"


# 4. PHOTO DE PROFIL
class Projetphotodeprofil(models.Model):
    images = models.ImageField(upload_to="static/images/", null=True, blank=True)
    est_visible = models.BooleanField(default=True, verbose_name="Afficher sur le site")

    class Meta:
        verbose_name = "Photo de profil"
        verbose_name_plural = "Photo de profil"

    def __str__(self):
        return f"Photo {self.id}"


# 5. A PROPOS DE MOI
class ProjetAproposDeMoi(models.Model):
    description = models.TextField(null=True, blank=False)
    est_visible = models.BooleanField(default=True, verbose_name="Afficher sur le site")

    class Meta:
        verbose_name = "À propos de moi"
        verbose_name_plural = "À propos de moi"

    def __str__(self):
        return self.description[:50] if self.description else f"A propos {self.id}"


# 6. COMPETENCES
class MesCompetencesCles(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=False)
    est_visible = models.BooleanField(default=True, verbose_name="Afficher sur le site")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ["nom"]

    def clean(self):
        self.nom = nettoyer_espaces(self.nom)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom if self.nom else f"Compétence {self.id}"


# 7. RESEAUX SOCIAUX
class ReseauSocial(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=255, blank=True, default="")
    est_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Réseau social"
        verbose_name_plural = "Réseaux sociaux"
        ordering = ["nom"]

    def clean(self):
        self.nom = nettoyer_espaces(self.nom)
        self.url = (self.url or "").strip()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
