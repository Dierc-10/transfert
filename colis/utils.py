from django.urls import resolve
from uuid import uuid4
from login.models import Agent, Province, Colis
from enum import Enum


class PROVINCE_ATTRIBUT(Enum):
    DESTINATAIRE= 0,
    EXPEDITEUR= 1

# Renvoie le nom de la page de la requête
def get_current_url_path(request):
    resolveMatcher = resolve(request.path)
    return resolveMatcher.url_name

# Genère l'ID Unique
def generate_unique_id():
    uid = uuid4().hex
    code = uid[:4].upper() + "-" + uid[4:8].upper()
    return code

# Renvoie les informations de l'utilisateur (Agent) en lien avec un User
def get_user_info(request):
    return Agent.objects.get(user=request.user)

# Récupère une donnée dans la requête faite par un utilisateur
# On vérifie dans la variable POST ou GET si la donnée voulu existe puis l'on renvoie sa valeur
def get_value_from_request(request,name,error_msg, value_type = str):
    try:    
        # Si la donnée existe .....
        if request.POST[name]:
            value = request.POST[name]
            
            # Si l'on veut récupérée la donnée comme chaines de caractères - String
            if value_type == str:
                return value
            
            # Si l'on veut récupérée la donnée comme nombre entier - Int 
            elif value_type == int: 
                return int(value)
            
            # Si l'on veut récupérée la donnée comme nombre flottant - Float
            elif value_type == float:
                return float(value)
            
    # En cas d'erreur, l'on renvoie le message d'erreur
    except: 
        if error_msg:
            raise Exception(error_msg)
        else:
            raise Exception(f"Erreur `{name}` n'existe pas !")
        
# Vérifie l'existe d'une province 
# Au cas où elle existe, l'on renvoie la donnée 
# Sinon l'on lève une erreur
def verify_and_get_province(id_province, error_msg):
    res = bool(Province.objects.get(id=id_province))
    
    if not res:
        raise Exception(error_msg)
    
    return Province.objects.get(id=id_province)

# Vérifie l'existance d'un Colis 
# Auc cas où il existe, l'on renvoie la donnée 
# Sinon l'on renvoie None par défaut
def verify_and_get_colis(colis_id:int, attribut: PROVINCE_ATTRIBUT, province:Province):
    
    try:
        # Si la province ciblée est celle du destinataire .....
        if attribut == PROVINCE_ATTRIBUT.DESTINATAIRE:
            return Colis.objects.get(id=colis_id, province_destinataire=province)
        
        # Si la province ciblée est celle de l'expéditeur ....
        elif attribut == PROVINCE_ATTRIBUT.EXPEDITEUR: 
            return Colis.objects.get(id=colis_id, province_expediteur=province)
        
        # Sinon, l'on renvoie None
        else:
            return None
        
    # Au cas où la donnée n'existe pas, on renvoie None
    except:
        return None