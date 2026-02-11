from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re

# Importations des modèles
from app_contact.models import User, Contact
from app_user.models import Menu, RoleMenuAcces


from app_contact.models import Role 

        # https://gemini.google.com/app/1b31b1ccfe391648
        # https://gemini.google.com/app/1b31b1ccfe391648





class GestionnaireUtilisateur:

    def creer_un_nouvel_utilisateur(self, request, nom_du_template):
        """Moteur central d'aiguillage selon le template source."""
        match nom_du_template:
            case "page_utilisateur.html":
                return self._add_user(request)
            case "index.html":
                return self._index_inscription_view(request)
            case _:
                return render(request, '404.html')



    def _Fonction_Page_gestion_des_Utilisateurs(self, request, erreurs_champs=None, donnees_saisies=None):
        """Rendu de la page admin users + permissions + contacts."""
        users = User.objects.select_related("role").all()
        menus = Menu.objects.all()
        contacts = Contact.objects.all().order_by("-date_envoi")
        roles = Role.objects.all()

        acces_existants = [
            f"{a.role_id}_{a.menu_id}"
            for a in RoleMenuAcces.objects.filter(est_visible=True)
        ]

        user_session = request.session.get("user")
        mes_menus_visibles = RoleMenuAcces.objects.none()  # ✅ mieux que []

        u = None
        if user_session and user_session.get("id"):
            u = User.objects.filter(id=user_session["id"]).select_related("role").first()
            if u and u.role_id:
                mes_menus_visibles = RoleMenuAcces.objects.filter(
                    role_id=u.role_id, est_visible=True
                ).select_related("menu")

        print(f"mes_menus_visibles = {mes_menus_visibles}")
        print(f"acces_existants = {acces_existants}")

        # ✅ Vérification correcte (sans boucle)
        autorise = False
        if u and u.role_id:
            autorise = RoleMenuAcces.objects.filter(
                role_id=u.role_id,
                est_visible=True,
                menu__nom="Gestion des Utilisateurs"
            ).exists()

        if autorise:
            print("L'OUVERTURE de la 'page_utilisateur.html' est AUTORISEE !")
            
            context = {
                "users": users,
                "menus": menus,
                "contacts": contacts,
                "roles": roles,
                "acces_existants": acces_existants,
                "mes_menus_visibles": mes_menus_visibles,
                "erreurs_champs": erreurs_champs or {},
                "donnees_saisies": donnees_saisies or {},
            }
            return render(request, "page_utilisateur.html", context)
            
        else:
            print("Accès refusé à 'page_utilisateur.html'")
            return redirect("name_acceuil")        # REDIRECTION vers la """"""""PAGE D'ACCEUIL"""""""" du Site Web du """"""""PORTFOLIO""""""""            # app_acceuil / urls.py         # Public        # path("index.html", aff_acceuil_PAGE_PUBLIQUE_Vue_par_les_VISITEURS, name="name_acceuil"),




    def _valider_email(self, email):
        """Vérifie le format de l'email via Regex."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+$'
        return bool(re.match(pattern, email))





# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""

# app_user > views.py

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""


    def _add_user(self, request):
        """Logique d'ajout d'un utilisateur avec validation."""
        erreurs_champs = {}
        donnees_saisies = {}

        if request.method == "POST":
            nom = request.POST.get('nom', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            nom_role_choisi = request.POST.get('role') # Ex: "Administrateur"
            
            donnees_saisies = {'nom': nom, 'email': email, 'role': nom_role_choisi}

            # --- VALIDATIONS ---
            if not nom: 
                erreurs_champs['nom'] = "Le nom est obligatoire."
            
            if not email or not self._valider_email(email):
                erreurs_champs['email'] = "Format d'email invalide. (Exemple : monemail@gmail.com)"
            elif User.objects.filter(email=email).exists():
                erreurs_champs['email'] = "Cet email appartient déjà à un compte."

            if not password:
                erreurs_champs['password'] = "Le mot de passe est obligatoire."
            
            elif len(password) < 6:
                erreurs_champs['password'] = "Le mot de passe doit faire au moins 6 caractères."

            if not nom_role_choisi: 
                erreurs_champs['role'] = "Le rôle est obligatoire."

            # --- ENREGISTREMENT ---
            if not erreurs_champs:
                try:
                    # 1. On récupère l'objet Role correspondant au nom sélectionné
                    # On utilise .get() car les rôles doivent déjà exister en base
                    role_obj = Role.objects.get(nom_role=nom_role_choisi)

                    # 2. On crée l'utilisateur en passant l'OBJET role_obj
                    User.objects.create(
                        nom=nom, 
                        email=email, 
                        password=make_password(password),
                        role=role_obj # On passe l'instance de Role ici
                    )
                    
                    messages.success(request, f"L'utilisateur {nom} ({nom_role_choisi}) a été créé !")
                    return redirect('gestion_globale') 
                    
                except Role.DoesNotExist:
                    erreurs_champs['role'] = "Le rôle sélectionné n'existe pas dans la base de données."
                except Exception as e:
                    erreurs_champs['global'] = f"Erreur technique : {e}"

        # Retourne le rendu avec les erreurs
        return self._Fonction_Page_gestion_des_Utilisateurs(request, erreurs_champs, donnees_saisies)



    def _Fonction_Page_gestion_des_UtilisateursEDIT(self, request, erreurs_champsEDIT=None, user_id_erreur=None , donnees_saisies=None , role_obj=None):
        users = User.objects.all()
        #   votre_template.html
        return render(request, 'page_utilisateur.html', {
            'users': users,
            'erreurs_champsEDIT': erreurs_champsEDIT,
            'user_id_erreur': user_id_erreur,
            'donnees_edit': donnees_saisies, # <-- On transmet au template
            'roles': role_obj
        })



    def edit_user(self, request, user_id):
        """Met à jour les informations d'un utilisateur existant."""
        erreurs_champs = {}
        donnees_saisies = {}        
        # On récupère l'utilisateur à modifier ou une erreur 404 s'il n'existe pas
        user = get_object_or_404(User, id=user_id)
        
        if request.method == "POST":
            # 1. Récupération des données du formulaire
            nouveau_nom = request.POST.get('nom', '').strip()
            nouvel_email = request.POST.get('email', '').strip()
            nouveau_mdp = request.POST.get('password', '').strip()
            nom_role_choisi = request.POST.get('role') # Le texte du rôle (ex: "Administrateur")

            # ÉTAPE CRUCIALE : Transformer le texte du rôle en objet Role (ForeignKey)

            role_objet = Role.objects.all()         # On affiche       """""TOUTES LES DONNEES"""""       contenues dans la      TABLE      """""app_contact_role"""""      ,     contenue dans l'APPLICATION DJANGO nommée     """""app_contact"""""     dans le fichier     """""models.py"""""     correspondant à la     """"class Role(models.Model):""""

            print(f"role_objet = {role_objet}")
            
            donnees_saisies = {'nom': nouveau_nom, 'email': nouvel_email, 'role': nom_role_choisi , 'roles': role_objet}


            # --- VALIDATIONS ---
            if not nouveau_nom: 
                erreurs_champs['nom'] = "Le nom est obligatoire."
            
            # Validation email : format + unicité (on exclut l'ID actuel pour permettre de garder son propre email)
            if not nouvel_email or not self._valider_email(nouvel_email):
                erreurs_champs['email'] = "Format d'email invalide. (Exemple : monemail@gmail.com)"
            elif User.objects.filter(email=nouvel_email).exclude(id=user_id).exists():
                erreurs_champs['email'] = "Cet email est déjà utilisé par un autre compte."

            if not nouveau_mdp:
                erreurs_champs['password'] = "Le mot de passe est obligatoire."
                            
            # Validation mot de passe (seulement s'il est modifié et n'est pas déjà un hash)
            if nouveau_mdp and not nouveau_mdp.startswith('pbkdf2_'):
                if len(nouveau_mdp) < 6:
                    erreurs_champs['password'] = "Le mot de passe doit faire au moins 6 caractères."

            if not nom_role_choisi: 
                erreurs_champs['role'] = "Le rôle est obligatoire."

            # --- TRAITEMENT ET ENREGISTREMENT ---
            if not erreurs_champs:
                try:
                    # ÉTAPE CRUCIALE : Transformer le texte du rôle en objet Role (ForeignKey)
                    role_obj = Role.objects.get(nom_role=nom_role_choisi)
                    
                    user.nom = nouveau_nom
                    user.email = nouvel_email
                    user.role = role_obj # On assigne l'instance d'objet
                    
                    # On ne change le mot de passe que si un nouveau a été saisi
                    if nouveau_mdp and not nouveau_mdp.startswith('pbkdf2_'):
                        user.password = make_password(nouveau_mdp)
                    
                    user.save()
                    messages.success(request, f"L'utilisateur {user.nom} ({role_obj.nom_role}) a été mis à jour avec succès.")
                    return redirect('gestion_globale')

                except Role.DoesNotExist:
                    erreurs_champs['role'] = "Le rôle sélectionné n'existe pas."
                except Exception as e:
                    messages.error(request, f"Erreur technique lors de la sauvegarde : {e}")
            
            # --- EN CAS D'ERREUR DE VALIDATION ---
            # On renvoie vers la fonction qui affiche la page avec les erreurs pour la modale
            return self._Fonction_Page_gestion_des_UtilisateursEDIT(
                request, 
                erreurs_champsEDIT=erreurs_champs, 
                user_id_erreur=user_id, # ID utilisé par le JS pour rouvrir la modale
                donnees_saisies=donnees_saisies,
                role_obj=role_objet           
            )

        # Si accès en GET, on redirige simplement
        return redirect('gestion_globale')

    def delete_user(self, request, user_id):
        """Supprime un utilisateur de la base."""
        if request.method == "POST":
            user = get_object_or_404(User, id=user_id)
            nom = user.nom
            role = user.role
            user.delete()
            messages.error(request, f"Utilisateur {nom} ({role}) supprimé définitivement.")
        return redirect('gestion_globale')

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""

# app_user > views.py

# REMARQUE IMPORTANTE :
######### Dans le FICHIER """"PackageUser/modul_new_user.py/class GestionnaireUtilisateur:"""" se trouvent les FONCTIONS (CRUD) """"def _add_user(self, request):"""" et """"def edit_user(self, request, user_id):"""" et """"def delete_user(self, request, user_id):""""

