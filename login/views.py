from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from login.models import Province, Agent
from django.contrib.auth.models import User
from colis.utils import verify_and_get_province
# Create your views here.

def connexion(request):
    erreur = None
    # Si l'utilisateur est déjà connecté,
    # alors on le rédirige vers la page `dashboard`
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # On recupère les informations envoyer par l'utilisateur 
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        province_id = request.POST.get('province')
        
        try:
            province = verify_and_get_province(id_province=province_id, error_msg="La province n'existe pas ou a été supprimée !")
            print("Province", province_id, province)
            agent = Agent.objects.get(name=username, mdp=password, province=province)
            print("Agent", agent)
            
            if agent:
                user = authenticate(username=username, password=password)
                if user: 
                    login(request, user)
                    return redirect('dashboard')
                else: 
                    erreur = "Contactez l'administrateur pour activer/affecter votre compte." 
            else: 
                erreur = "Username, mot de passe ou province incorrect !"
        
        except Exception as err : 
            erreur = "Username, mot de passe ou province incorrect !"
        
     
    provinces =  Province.objects.all()
    return render(request, 'login.html', context={"provinces": provinces, "erreur": erreur})

def deconnexion(request):
    logout(request)
    return redirect('dashboard')