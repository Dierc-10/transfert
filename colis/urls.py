"""colis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from login.views import connexion, deconnexion
from .views import dashboard, liste_reception as receptions, liste_transfert as transferts, checkup, nouveau, bordereau_retrait, bordereau_transfert, supprimer_colis

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", connexion, name="connexion"),
    path("dashboard/", dashboard , name="dashboard"), 
    path("deconnexion/", deconnexion, name="deconnexion"), 
    path("receptions/", receptions , name="receptions"),
    path("transferts/", transferts , name="transferts"),
    path("checkup/", checkup , name="checkup"), 
    path("nouveau/", nouveau , name="nouveau"), 
    
    path("bordereau/retrait/<int:colis_id>", bordereau_retrait, name="bordereau_retrait"), 
    path("bordereau/transfert/<int:colis_id>", bordereau_transfert, name="bordereau_transfert"), 
    path("colis/supprimer/<int:colis_id>", supprimer_colis, name="supprimer_colis"),
    path("colis/supprimer/<int:colis_id>/<str:callback>", supprimer_colis, name="supprimer_colis")
]
