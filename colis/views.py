from django.shortcuts import redirect, render
from django.urls import resolve
from login.models import Agent, Colis, Destinataire, Expediteur, Province
from .utils import generate_unique_id, get_current_url_path, get_user_info, get_value_from_request, verify_and_get_province, verify_and_get_colis
from .utils import PROVINCE_ATTRIBUT
from datetime import date

def dashboard(request):
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect('connexion')
    
    return render(request, "dashboard.html", context=
        {
            "current_user": get_user_info(request) # Informations de l'utilisateur courrante
        }
    )

def liste_reception(request):
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect("connexion")
    
    # Récupération des informations de l'utilisateur courrante
    current_user = get_user_info(request)
    
    try:
        receptions = []
        # On récupère la liste de tous les colis
        # On filtre les colis qui ont comme `province_destinataire` la province de l'utilisateur courrante
        # On Ajoute ces derniers dans une liste que l'on va renvoyer à l'utilisateur
        for colis in Colis.objects.all().order_by("-date_enregistrement"):
            if colis.province_destinataire == (get_user_info(request)).province:
                receptions.append(colis)
    except:
        receptions = []
    
    return render(request, 'liste_reception.html', context=
        {
            "current_path": get_current_url_path(request), # Le nom de la page courrante
            "receptions" : receptions # Liste des Colis réceptionné
        }
    )

def liste_transfert(request):
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect("connexion")
    
    try:
        transferts = []
        # On récupère la liste de tous les colis
        # On filtre les colis qui ont comme `province_expediteur` la province de l'utilisateur courrante
        # On Ajoute ces derniers dans une liste que l'on va renvoyer à l'utilisateur
        for colis in Colis.objects.all().order_by("-date_enregistrement"):
            if colis.province_expediteur == (get_user_info(request)).province:
                transferts.append(colis)
    except:
        transferts = []
        
    return render(request, 'liste_transfert.html', context=
        {
            "current_path": get_current_url_path(request), # Le nom de la page courrante 
            "transferts": transferts # Liste des Colis transférés
        }
    )

def checkup(request):
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect('connexion')
    
    colis = None
    erreur = None
    
    if request.method == "POST":
        try:
            code = get_value_from_request(request=request, name="code", error_msg="Le code du colis est obligatoire pour checkup !", value_type=str)
            colis = Colis.objects.get(code=code.strip())
            return redirect("bordereau_retrait", colis_id=colis.id)
        except:
            erreur = "Aucun colis n'a été trouvé"
    
    return render(request, 'checkup.html', context=
        {
            "current_path": get_current_url_path(request), # Le nom de la page courrante 
            "erreur": erreur, # Message d'erreur
        }
    )


def nouveau(request):
    erreur = None
    success = None
    
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect('connexion')
    
    if request.method == "POST":
        try:
            # Donnée du colis
            code = get_value_from_request(request=request, name="code", error_msg="Le code du colis est obligatoire !")
            frais = get_value_from_request(request=request, name="frais", error_msg="Le champs frais est obligatoire - Type : Nombre ", value_type=float)
            poids = get_value_from_request(request=request, name="poids", error_msg="Le champs poids est obligatoire - Type : Nombre", value_type=float)
            observation = get_value_from_request(request=request, name="observation", error_msg="Le champs observation est obligatoire", value_type=str)
            # Données de l'expéditeur !
            expediteur_name = get_value_from_request(request=request, name="expediteur_name", error_msg="Le nom de l'expéditeur est obligatoire !")
            expediteur_prenom = get_value_from_request(request=request, name="expediteur_prenom", error_msg="Le prenom de l'expéditeur est obligatoire !")
            expediteur_province = get_value_from_request(request=request, name="expediteur_province", error_msg="La province de l'expéditeur est obligatoire", value_type=int)
            expediteur_telephone = get_value_from_request(request=request, name="expediteur_telephone", error_msg="Le telephone de l'expéditeur est obligatoire")
            expediteur_email = get_value_from_request(request=request, name="expediteur_email", error_msg="L'email de l'expéditeur est obligatoire")
            
            # Données du destinataire
            destinataire_name = get_value_from_request(request=request, name="destinataire_name", error_msg="Le nom du destinataire est obligatoire")
            destinataire_prenom = get_value_from_request(request=request, name="destinataire_prenom", error_msg="Le prenom du destinataire est obligatoire")
            destinataire_telephone = get_value_from_request(request=request, name="destinataire_telephone", error_msg="le telephone du destinataire est obligatoire")
            destinataire_province = get_value_from_request(request=request, name="destinataire_province", error_msg="La province du destinataire est obligatoire", value_type=int)
            destinataire_address = get_value_from_request(request=request, name="destinataire_address", error_msg="L'adresse du destinataire est obligatoire")
            destinataire_email = get_value_from_request(request=request, name="destinataire_email", error_msg="L'email du destinataire est obligatoire")
            
            province_expediteur = verify_and_get_province(expediteur_province, "La province de l'expéditeur n'existe pas ou a été supprimé")
            province_destinataire = verify_and_get_province(destinataire_province, "La province du destinataire n'existe pas ou a été supprimé")
            
            # Création et enregistrement de l'expéditeur
            expediteur =  Expediteur.objects.create(
                name=expediteur_name, 
                prenom=expediteur_prenom,
                gmail=expediteur_email,
                telephone=expediteur_telephone
            )
            
            # Création et enregistrement du destinataire
            destinataire = Destinataire.objects.create(
                name = destinataire_name, 
                prenom= destinataire_prenom, 
                telephone=destinataire_telephone, 
                gmail=destinataire_email, 
                adresse=destinataire_address
            )
            
            # Création et enregistrement du Colis
            colis = Colis.objects.create(
                name = code,
                frais = frais, 
                code = code , 
                poids=poids ,
                province_destinataire=province_destinataire, 
                province_expediteur=province_expediteur, 
                expediteur=expediteur ,
                destinataire=destinataire, 
                observation=str(observation).strip()
            )
            
            success = f"L'enregistrement {code} a réussi avec succès !"
        
        # En cas d'erreur, on le récupère le message d'erreur puis on le renvoie vers page !
        except Exception as err:
            if(len(err.args) > 1):
                success =  err.args[0]
            else:
                erreur = err.args[0]

    return render(request, 'nouveau.html', context=
        {
            "code": generate_unique_id() , # Universal Unique ID (uuid)
            "current_path": get_current_url_path(request), # le nom de la page current
            "provinces" : Province.objects.all(), # liste des provinces
            "current_user" : get_user_info(request), # Informations de l'utilisateur courante
            "erreur": erreur, # Message d'erreur
            "success": success # Message de succès
        }
    )

def bordereau_retrait(request, colis_id):
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect('connexion')
    
    erreur = None
    
    # Récupération d'information de l'utilisateur Agent - User
    user_info = get_user_info(request)
    
    # Vérification de l'existance du colis
    # Si ce dernier a été supprimé, l'on renvoie None
    colis = verify_and_get_colis(colis_id=colis_id, attribut=PROVINCE_ATTRIBUT.DESTINATAIRE, province=user_info.province)
    
    # Si le colis n'existe pas ou a été supprimé, l'on créee le message d'erreur
    if not colis: 
        erreur = "Ce colis n'existe pas ou a été supprimé"
    
    return render(request, "bordereau_retrait.html", context={"colis": colis, "erreur": erreur})

def bordereau_transfert(request, colis_id):
    erreur = None
    success = None
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect('connexion')
    
    erreur = None
    
    # Récupération d'information de l'utilisateur Agent - User
    user_info = get_user_info(request)
    
    # Vérification de l'existance du colis
    # Si ce dernier a été supprimé, l'on renvoie None
    colis = verify_and_get_colis(colis_id=colis_id, attribut=PROVINCE_ATTRIBUT.EXPEDITEUR, province=user_info.province)
    
    # Si le colis n'existe pas ou a été supprimé, l'on créee le message d'erreur 
    if not colis: 
        erreur = "Ce colis n'existe pas ou a été supprimé"
        
        
    if request.method == "POST":
        try:
            # Donnée du colis
            frais = get_value_from_request(request=request, name="frais", error_msg="Le champs frais est obligatoire - Type : Nombre ", value_type=float)
            poids = get_value_from_request(request=request, name="poids", error_msg="Le champs poids est obligatoire - Type : Nombre", value_type=float)
            observation = get_value_from_request(request=request, name="observation", error_msg="Le champs observation est obligatoire", value_type=str)
            date_enregistrement = get_value_from_request(request=request, name="date_enregistrement", error_msg="La date d'enregistrement est obligatoire ! ", value_type=str)
            
            # Données de l'expéditeur !
            expediteur_name = get_value_from_request(request=request, name="expediteur_name", error_msg="Le nom de l'expéditeur est obligatoire !")
            expediteur_prenom = get_value_from_request(request=request, name="expediteur_prenom", error_msg="Le prenom de l'expéditeur est obligatoire !")
            expediteur_telephone = get_value_from_request(request=request, name="expediteur_telephone", error_msg="Le telephone de l'expéditeur est obligatoire")
            expediteur_email = get_value_from_request(request=request, name="expediteur_email", error_msg="L'email de l'expéditeur est obligatoire")
            
            # Données du destinataire
            destinataire_name = get_value_from_request(request=request, name="destinataire_name", error_msg="Le nom du destinataire est obligatoire")
            destinataire_prenom = get_value_from_request(request=request, name="destinataire_prenom", error_msg="Le prenom du destinataire est obligatoire")
            destinataire_telephone = get_value_from_request(request=request, name="destinataire_telephone", error_msg="le telephone du destinataire est obligatoire")
            destinataire_province = get_value_from_request(request=request, name="destinataire_province", error_msg="La province du destinataire est obligatoire", value_type=int)
            destinataire_address = get_value_from_request(request=request, name="destinataire_address", error_msg="L'adresse du destinataire est obligatoire")
            destinataire_email = get_value_from_request(request=request, name="destinataire_email", error_msg="L'email du destinataire est obligatoire")
            
            province_destinataire = verify_and_get_province(destinataire_province, "La province du destinataire n'existe pas ou a été supprimé")
            
            # Mise à jour de l'expéditeur 
            expediteur = Expediteur.objects.get(id=colis.expediteur.id) 
            expediteur.name = expediteur_name
            expediteur.prenom = expediteur_prenom 
            expediteur.gmail = expediteur_email 
            expediteur.telephone = expediteur_telephone
            expediteur.save() # Sauvegarde des mises à jours
            
            # Mise à jour du destinataire 
            destinataire = Destinataire.objects.get(id=colis.destinataire.id)
            destinataire.name = destinataire_name
            destinataire.prenom = destinataire_prenom
            destinataire.telephone = destinataire_telephone
            destinataire.gmail = destinataire_email
            destinataire.adresse = destinataire_address
            destinataire.save() # Sauvegarde des mises à jours 
            
            # Mise à jour du Colis
            colis.frais = frais 
            colis.poids=poids 
            colis.date_enregistrement= date.fromisoformat(date_enregistrement)
            colis.province_destinataire=province_destinataire 
            colis.observation=str(observation).strip()
            colis.save() # Sauvegarde des mises à jours
            
            success = "La modification a réussi avec succès !"
        
        # En cas d'erreur, on le récupère le message d'erreur puis on le renvoie vers page !
        except Exception as err:
            if(len(err.args) > 1):
                success =  err.args[0]
            else:
                erreur = err.args[0]
    
    return render(request, "bordereau_transfert.html", context={
        "colis": colis, # Colis récupéré 
        "erreur": erreur, # Message d'erreurto
        "current_path": get_current_url_path(request), # Le nom de la page courrante
        "provinces": Province.objects.all()
        }
    )
    
def supprimer_colis(request, colis_id, callback=None):
    # Si l'utilisateur n'est pas connecté (authentifié), on le redirige vers la page de connexion
    if not request.user.is_authenticated:
        return redirect('connexion')
    
    # Suppresion du colis 
    try:
        colis = Colis.objects.get(id=colis_id)
        colis.delete()
    except:
        pass
        
    # Le callback est l'adresse de la page a appellé après la suppresion du colis
    # Si ce dernier existe, alors on redirige l'utilisateur vers cette page
    # Sinon l'on le redirige vers la page `dashboard`
    if callback:
        return redirect(callback)
    else :
        return redirect("dashboard")