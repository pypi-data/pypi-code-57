from django.conf import settings
from django.db import models
from djangoldp.models import Model
from django.contrib.auth import get_user_model

class Type (Model):
    name = models.CharField(max_length=50, verbose_name="Resource type")

    class Meta : 
        anonymous_perms = ['view', 'add']

    def __str__(self):
        return self.name

class Keyword (Model):
    name = models.CharField(max_length=50, verbose_name="Keywords")
    
    class Meta : 
        anonymous_perms = ['view', 'add']
 
    def __str__(self):
        return self.name


class Resource (Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)
    name = models.CharField(max_length=50, verbose_name="Resource Title")
    shortdesc = models.TextField(blank=True, null=True)
    longdesc = models.TextField(blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    type = models.ForeignKey(Type, blank=True, null=True,verbose_name="Resource type")
    img = models.URLField(default="/media/defaultresource.png", verbose_name="Illustration")
    document = models.URLField(blank=True, null=True, verbose_name="Document")
    link = models.CharField(max_length=150, blank=True, null=True, verbose_name="Internet link")

    class Meta : 
        serializer_fields=["@id", "name", "shortdesc", "longdesc", "type", "img", "document",\
                           "link", "keywords"]
        # auto_author = 'user'
        # owner_field = 'user'
        container_path = 'resources/'
        rdf_type = 'hd:resource'
        anonymous_perms = ['view', 'add']
        owner_perms = ['inherit', 'change', 'control', 'delete']
        authenticated_perms = ['inherit', 'add']
        nested_fields = ['keywords']
        
    def __str__(self):
        return self.name