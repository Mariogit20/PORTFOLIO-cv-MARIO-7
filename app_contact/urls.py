from django.urls import path
from .views import *



urlpatterns = [
    # Page principale qui gère l'affichage de base et l'inscription

    path('root_gemini_accueil', index_inscription_view, name='root_gemini_accueil'),    

    path('connexion/', login_view, name='loginpage'),
    
    path('deconnexion/', deconexion_view, name='deconexion'),
    

    
    path('page_inscription' , page_inscription , name="page_inscription")
]
