



from django.db import models



# https://gemini.google.com/app/4087d09848fdd4b6
# https://gemini.google.com/app/c25ec29c52442407
# https://gemini.google.com/app/822028a316d61568




class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):                     # CHAMP    """""email"""""    TOUJOURS    EN    """""MINUSCULE"""""
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom


# //        window.location.href = "/";       //  Garde l'historique ?  Oui      //  Navigation standard entre les pages.



# // On ""RECHARGE COMPLETEMENT"" la ""PAGE D'ACCUEIL"" nommé ""index.html"" afin de """"FAIRE APPARAITRE"""" les """"IMAGES"""" contenues dans le FICHIER """"index.html"""" :::::::::::::::::::::::::

# ///// window.location.href = "/"       //  Garde l'historique ?  Oui      //  Navigation standard entre les pages.








# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e



        # https://gemini.google.com/app/1332cca0d76a0b1e
        # https://gemini.google.com/app/1332cca0d76a0b1e
        # https://gemini.google.com/app/1332cca0d76a0b1e
        # https://gemini.google.com/app/1332cca0d76a0b1e      




# https://gemini.google.com/app/bbba657c1b185397
# https://gemini.google.com/app/bbba657c1b185397
# https://gemini.google.com/app/bbba657c1b185397
# https://gemini.google.com/app/bbba657c1b185397
# https://gemini.google.com/app/bbba657c1b185397



# https://gemini.google.com/app/e90aa1b5c8659267
# https://gemini.google.com/app/e90aa1b5c8659267
# https://gemini.google.com/app/e90aa1b5c8659267
# https://gemini.google.com/app/e90aa1b5c8659267




# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494




# page_inscription.html

# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494
# https://gemini.google.com/app/f7b714a644fad494 





# https://gemini.google.com/app/cbb617324b1498ce
# https://gemini.google.com/app/cbb617324b1498ce
# https://gemini.google.com/app/cbb617324b1498ce
# https://gemini.google.com/app/cbb617324b1498ce
# https://gemini.google.com/app/cbb617324b1498ce





# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e
# https://gemini.google.com/app/1332cca0d76a0b1e



        # https://gemini.google.com/app/1332cca0d76a0b1e
        # https://gemini.google.com/app/1332cca0d76a0b1e
        # https://gemini.google.com/app/1332cca0d76a0b1e
        # https://gemini.google.com/app/1332cca0d76a0b1e      








# # Étapes à suivre pour appliquer le changement

# # Une fois que vous avez modifié votre fichier models.py, vous devez impérativement mettre à jour votre base de données :

# #     Créer la migration : python manage.py makemigrations

# #     Appliquer la migration : python manage.py migrate

# #     [!CAUTION] Attention : Si votre base de données contient déjà des doublons (deux utilisateurs avec le même email), la migration va échouer. Vous devrez d'abord supprimer ou modifier les doublons manuellement avant de lancer migrate.
    


# https://gemini.google.com/app/f1c52fba06c87797
# https://gemini.google.com/app/f1c52fba06c87797    
    

# 1. MODÈLE DES RÔLES
class Role(models.Model):
    nom_role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom_role



# 2. MODÈLE DES UTILISATEURS
class User(models.Model):
    nom = models.CharField(max_length=100, blank=False, null=False)        #       , blank=False, null=False           signifie   """"interdire email vide""""   c'est-à-dire   """"rendre l’email obligatoire""""
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False) # Stocke le hash
    # Relation ForeignKey vers Role
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="utilisateurs", blank=False, null=False)       # on_delete=models.CASCADE veut dire : supprimer un rôle ⇒ supprime tous les utilisateurs liés. Souvent dangereux.

    def save(self, *args, **kwargs):                     # CHAMP    """""email"""""    TOUJOURS    EN    """""MINUSCULE"""""
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.role.nom_role})"
    

#################################################################################################

# OK, avec SQLite :

# Ton save() qui fait lower() est parfait et suffisant dans la majorité des cas ✅

# Mais attention : unique=True dans SQLite est sensible à la casse selon les collations, donc sans normalisation, Test@x.com et test@x.com pourraient coexister. Avec ton save(), tu empêches ça.
    
#################################################################################################    
                
#      Le code suivant est t il correct : 
# # 2. MODÈLE DES UTILISATEURS
# class User(models.Model):
#     nom = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255) # Stocke le hash
#     # Relation ForeignKey vers Role
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="utilisateurs")

#     def save(self, *args, **kwargs):
#         if self.email:
#             self.email = self.email.strip().lower()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.nom} ({self.role.nom_role})"
    
    
    
                

# Oui — ce code est correct pour forcer l’email en minuscule à chaque sauvegarde. ✅
# Mais il y a 2–3 points à connaître pour éviter des soucis en prod.

# Ce qui est bon

# self.email = self.email.strip().lower() : nickel, ça normalise bien.

# super().save(*args, **kwargs) : ok.

# Petites améliorations recommandées
# 1) Évite de supprimer des users si un Role est supprimé

# on_delete=models.CASCADE veut dire : supprimer un rôle ⇒ supprime tous les utilisateurs liés. Souvent dangereux. Préfère :

# models.PROTECT (recommandé) ou

# models.SET_NULL (si tu autorises rôle nul)

# role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="utilisateurs")

# 2) __str__ peut planter si role est nul (si un jour tu passes en SET_NULL)

# Si tu gardes CASCADE/PROTECT, pas de souci. Sinon fais :

# def __str__(self):
#     role = self.role.nom_role if self.role else "Sans rôle"
#     return f"{self.nom} ({role})"

# 3) Bonus important : unicité insensible à la casse (cas limites)

# Ton .lower() empêche la plupart des doublons, mais le top (surtout si plusieurs insertions concurrentes ou déjà des données) est une contrainte DB insensible à la casse (PostgreSQL) :

# from django.db.models.functions import Lower
# from django.db import models

# class Meta:
#     constraints = [
#         models.UniqueConstraint(Lower("email"), name="uniq_user_email_lower")
#     ]

# Version finale (simple et robuste)
# class User(models.Model):
#     nom = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="utilisateurs")

#     def save(self, *args, **kwargs):
#         if self.email:
#             self.email = self.email.strip().lower()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.nom} ({self.role.nom_role})"


# Si tu me dis ta base (PostgreSQL/MySQL/SQLite), je te dis si la contrainte Lower(email) est possible et comment faire la migration proprement.

# sqlite

# OK, avec SQLite :

# Ton save() qui fait lower() est parfait et suffisant dans la majorité des cas ✅

# Mais attention : unique=True dans SQLite est sensible à la casse selon les collations, donc sans normalisation, Test@x.com et test@x.com pourraient coexister. Avec ton save(), tu empêches ça.

# Recommandation (SQLite)
# 1) Garde ton save() (comme tu l’as fait)

# C’est la solution la plus simple et fiable pour ton cas.

# 2) Ajoute aussi une validation côté formulaire/serializer (optionnel mais mieux)

# Ça te donne un message d’erreur propre avant de tenter la sauvegarde.

# Django Form / ModelForm :

# def clean_email(self):
#     return self.cleaned_data["email"].strip().lower()


# DRF Serializer :

# def validate_email(self, value):
#     return value.strip().lower()

# Et la contrainte Lower(email) ?

# Tu peux techniquement écrire UniqueConstraint(Lower("email")), mais sur SQLite ce n’est pas aussi “standard”/robuste qu’en PostgreSQL selon les versions et le support des index d’expressions. Donc, dans ton cas, je te conseille de rester sur le save() + validation.

# Petit bonus : rendre l’email obligatoire

# Si tu veux interdire email vide :

# email = models.EmailField(unique=True, blank=False, null=False)


# (EmailField est déjà blank=False par défaut, mais ça rend l’intention claire.)

# En bref : oui ton code est correct pour SQLite.
# Si tu utilises des endpoints API (DRF) ou des formulaires, je te conseille d’ajouter aussi la normalisation dans clean_email()/validate_email() pour une UX plus propre.



           