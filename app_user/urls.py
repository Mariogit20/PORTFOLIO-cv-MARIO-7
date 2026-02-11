

# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1
# # https://gemini.google.com/app/067aeb3e6aaa6bc1


from django.urls import path
from .views import * # Importe vos autres vues (edit, delete, update)
from PackageUser.modul_new_user import GestionnaireUtilisateur

# On instancie le gestionnaire
gestionnaire = GestionnaireUtilisateur()

urlpatterns = [
    # Page principale : On pointe vers la méthode de rendu
    # Note : On utilise une fonction lambda ou on s'assure que la méthode 
    # est accessible. La façon la plus propre en Django "Function Based Views" 
    # avec une classe est d'appeler la méthode de l'instance.
    
    path('root_gestion_utilisateur/', 
         lambda request: gestionnaire._Fonction_Page_gestion_des_Utilisateurs(request), 
         name='gestion_globale'),

    # Action Ajout Utilisateur : On utilise votre moteur central
    path('user/add/', 
         lambda request: gestionnaire.creer_un_nouvel_utilisateur(request, "page_utilisateur.html"), 
         name='add_user'),



    path('user/edit/<int:user_id>/', 
         lambda request, user_id: gestionnaire.edit_user(request, user_id), 
         name='edit_user'),
         
    path('user/delete/<int:user_id>/', 
         lambda request, user_id: gestionnaire.delete_user(request, user_id), 
         name='delete_user'),
    
    # Action Permissions
    path('user/update-menus/', update_menus, name='update_menus'),
]



