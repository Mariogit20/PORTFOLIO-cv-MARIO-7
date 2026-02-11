"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

# MICKAEL Hopes Formation Andavamamba , Formation PYTHON Spécial SAMEDI durant SEPT MOIS
from django.conf import settings                    # MICKAEL Hopes Formation Andavamamba , Formation PYTHON Spécial SAMEDI durant SEPT MOIS

# MICKAEL Hopes Formation Andavamamba , Formation PYTHON Spécial SAMEDI durant SEPT MOIS
from django.conf.urls.static import static                    # MICKAEL Hopes Formation Andavamamba , Formation PYTHON Spécial SAMEDI durant SEPT MOIS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("app_acceuil.urls")),
    path('',include("app_contact.urls")),
    # path('',include("app_connection.urls")),
    path('',include("app_user.urls")),
    path('',include("app_historique.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:                    # MICKAEL Hopes Formation Andavamamba , Formation PYTHON Spécial SAMEDI durant SEPT MOIS
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                    # MICKAEL Hopes Formation Andavamamba , Formation PYTHON Spécial SAMEDI durant SEPT MOIS

