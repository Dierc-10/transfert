from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.
class Expediteur(models.Model):
    name = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    gmail = models.CharField(max_length=200)
    
    @classmethod
    def ajouter(self):
        pass 
    
    @classmethod
    def modofier(self):
        pass 
    
    @classmethod
    def supprimer(self):
        pass
    
    @classmethod
    def recherche(self):
        pass
    
    @classmethod
    def imprimer(selft):
        pass

    class Meta:
        verbose_name = "expediteur"
        verbose_name_plural = "expediteurs"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("expediteur_detail", kwargs={"pk": self.pk})

class Destinataire(models.Model):
    name = models.CharField(max_length=200, null=False)
    prenom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    gmail = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    
    @classmethod
    def ajouter(self):
        pass 
    
    @classmethod
    def supprimer(self):
        pass
    
    @classmethod
    def rechercher(self):
        pass
    
    @classmethod
    def imprrimer(self):
        pass

    class Meta:
        verbose_name = "destinataire"
        verbose_name_plural = "destinataires"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("destinataire_detail", kwargs={"pk": self.pk})

class Province(models.Model):
    name = models.CharField(max_length=200, null=False)
    
    @classmethod
    def get_all(self):
        return ["kin", "test"]
    
    @classmethod
    def consulter(self):
        pass
    
    @classmethod
    def ajouter(self):
        pass
    
    @classmethod
    def rechercher(self):
        pass
    
    @classmethod
    def modifier(self):
        pass
    
    @classmethod
    def supprimer(self):
        pass

    class Meta:
        verbose_name = "province"
        verbose_name_plural = "provinces"

    def __str__(self):
        return self.name

    def get_absolute_url(seAgentlf):
        return reverse("province_detail", kwargs={"pk": self.pk})

class Colis(models.Model):
    name = models.CharField(max_length=200)
    frais = models.FloatField()
    poids = models.FloatField()
    date_enregistrement = models.DateField(default=datetime.date.today)
    expediteur = models.OneToOneField(Expediteur, on_delete=models.DO_NOTHING)
    destinataire = models.OneToOneField(Destinataire, on_delete=models.DO_NOTHING)
    province_expediteur = models.ForeignKey(Province,related_name='province_origine' ,on_delete=models.DO_NOTHING)
    province_destinataire = models.ForeignKey(Province,related_name='province_destination' ,on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=200)
    observation = models.CharField(max_length=255, default="", null=True)
    
    @classmethod
    def transfert(self):
        pass 
    
    @classmethod
    def imprimer_bon(self):
        pass
    
    @classmethod
    def rechercher_bon(self):
        pass 
    
    @classmethod
    def annuler_transfert(self):
        pass 
    
    @classmethod
    def editier_transfert(self):
        pass 
    
        
    class Meta:
        verbose_name = "colis"
        verbose_name_plural = "colis"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("colis_detail", kwargs={"pk": self.pk})

class Agent(models.Model):
    name =  models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    profil = models.CharField(max_length=200)
    mdp = models.CharField(max_length=200)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    province = models.OneToOneField(Province, on_delete=models.CASCADE)

    @classmethod
    def authentification(self):
        pass
    
    @classmethod
    def enregistrer(self):
        pass
    
    @classmethod
    def modifier(self):
        pass 
    
    @classmethod
    def supprimer(self):
        pass 
    
    class Meta:
        verbose_name = "agent"
        verbose_name_plural = "agents"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("agent_detail", kwargs={"pk": self.pk})
