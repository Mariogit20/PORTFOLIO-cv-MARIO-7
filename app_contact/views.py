from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Contact, User
import re

# --- CONFIGURATION ET UTILITAIRES ---

# Pattern pour valider une adresse email
pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+$'

def valider_email(email):
    if re.match(pattern, email):
        return True
    return False

# --- VUES DES PAGES ---

def page_inscription(request):
    """Affiche la page d'inscription simple."""
    return render(request, "page_inscription.html")

def aff_contact(request):
    """Affiche la liste des contacts sur la page index."""
    listeContact = Contact.objects.all()
    contenu = {
        "formation": listeContact
    }
    return render(request, "index.html", contenu)

# --- LOGIQUE D'INSCRIPTION AVEC RÔLE ---


from .models import Role  # N'oubliez pas d'importer Role

def index_inscription_view(request):
    erreurs_champs = {}
    donnees_saisies = {}

    if request.method == "POST":
        # 1. Récupération des données
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        nom_role_choisi = request.POST.get('role', 'Utilisateur') 

        donnees_saisies = {
            'nom': nom, 
            'email': email,
            'role': nom_role_choisi
        }

        # 2. Validations (Nom, Email, Password)
        if not nom:
            erreurs_champs['nom'] = "Le nom est obligatoire."
        
        if not email or not valider_email(email):
            erreurs_champs['email'] = "Format d'email invalide. (Exemple : monemail@gmail.com)"
        elif User.objects.filter(email=email).exists():
            erreurs_champs['email'] = "Cet email est déjà utilisé par un autre compte."

        if not password:
            erreurs_champs['password'] = "Le mot de passe est obligatoire."
        elif len(password) < 6:
            erreurs_champs['password'] = "Le mot de passe doit faire au moins 6 caractères."

        # 3. Traitement du Rôle et Enregistrement
        if not erreurs_champs:
            try:
                # CRUCIAL : On récupère l'objet Role en base de données
                # On utilise get_or_create pour éviter une erreur si le rôle n'existe pas encore
                role_obj, created = Role.objects.get_or_create(nom_role=nom_role_choisi)
                
                nouvel_utilisateur = User(
                    nom=nom,
                    email=email,
                    role=role_obj, # On passe l'objet Role, pas le texte
                    password=make_password(password)
                )
                nouvel_utilisateur.save()
                
                # Connexion en session (on stocke le texte pour la session)
                request.session['user'] = {
                    'id': nouvel_utilisateur.id, 
                    'nom': nouvel_utilisateur.nom,
                    'role': role_obj.nom_role
                }
                
                messages.success(request, f"Félicitations {nom}, votre compte {role_obj.nom_role} est prêt !")
                return redirect('/#accueil')
            
            except Exception as e:
                erreurs_champs['global'] = f"Erreur technique : {str(e)}"

    return render(request, 'index.html', {
        'erreurs_champs': erreurs_champs,
        'donnees': donnees_saisies
    })

# --- LOGIQUE DE CONNEXION ---

def login_view(request):
    erreurs = {}
    if request.method == 'POST':
        email_saisi = request.POST.get('email', '').strip().lower()
        password_saisi = request.POST.get('password', '')

        try:
            user = User.objects.get(email=email_saisi)

            # Vérification du mot de passe haché
            if check_password(password_saisi, user.password):
                # Création de la session
                request.session['user'] = {
                    'id': user.id, 
                    'nom': user.nom,
                    'email': user.email,
                    'role': user.role.nom_role  # On stocke uniquement le texte (ex: "Administrateur")      # On ajoute le rôle en session
                }
                messages.success(request, f"Ravi de vous revoir {user.nom} ({user.role}) !")
                return redirect('/#accueil')
            else:
                erreurs['login'] = "Email ou mot de passe incorrect."
        
        except User.DoesNotExist:
            erreurs['login'] = "Email ou mot de passe incorrect."

    return render(request, 'login.html', {
        'erreurs_saisi_identification_login_password_user': erreurs
    })

# --- LOGIQUE DE DÉCONNEXION ---

def deconexion_view(request):
    if 'user' in request.session:
        # Nettoyage complet de la session
        request.session.flush()
    return redirect('name_acceuil')


    