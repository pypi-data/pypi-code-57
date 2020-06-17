from django.conf import settings
from django.db import models
from djangoldp.models import Model

       
class Typeevent (Model):
    name = models.CharField(max_length=20, verbose_name="Type d'évènement")

    class Meta : 
        anonymous_perms = ['view', 'add']
    
    def __str__(self):
        return self.name

class Locationevent (Model):
    name = models.CharField(max_length=50, verbose_name="Lieu, établissement")
    address = models.TextField(max_length=225, blank=True, null=True, verbose_name="Adresse")

    class Meta : 
        anonymous_perms = ['view', 'add']
    
    def __str__(self):
        return self.name


class Event (Model):
    name = models.CharField(max_length=50, verbose_name="Nom de l'évènement")
    type = models.ForeignKey(Typeevent, verbose_name="Type d'évènement")
    startDate =  models.DateField(verbose_name="Date de début")
    startTime = models.TimeField(verbose_name="Heure de début")
    endDate =  models.DateField(verbose_name="Date de fin",blank=True, null=True )
    endTime =  models.TimeField(verbose_name="Heure de fin",blank=True, null=True )
    img = models.URLField(blank=True, null=True, verbose_name="Illustration de l'évènement")
    location = models.ForeignKey(Locationevent, blank=True, null=True, verbose_name="Lieu de l'évènement")
    shortDescription = models.CharField(max_length=250,verbose_name="Short description")
    longDescription = models.TextField(verbose_name="Long description")
    link = models.CharField(max_length=150, blank=True, null=True, verbose_name="Lien internet")
    facebook = models.CharField(max_length=150, blank=True, null=True, verbose_name="Lien Facebook")

    class Meta : 
        nested_fields=['type']
        ordering = ["startDate"]
        anonymous_perms = ['view', 'add']
        
    def __str__(self):
        return self.name
