from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Status(models.Model):
    status = models.BooleanField(null=True, default=True)
    class Meta:
        abstract = True


class DatLog(Status):
    dat_insercao = models.DateTimeField(auto_now_add=True, null=True)
    dat_edicao = models.DateTimeField(auto_now=True, null=True)
    dat_delete = models.DateTimeField(null=True)
    class Meta:
        abstract = True


class UsrLog(Status):
    usr_insercao = models.ForeignKey('nico.Profile', on_delete=models.SET_NULL, null=True, related_name='usr_insercao')
    usr_edicao = models.ForeignKey('nico.Profile', on_delete=models.SET_NULL, null=True, related_name='usr_edicao')
    usr_delete = models.ForeignKey('nico.Profile', on_delete=models.SET_NULL, null=True, related_name='usr_delete')
    class Meta:
        abstract = True


class Log(DatLog, UsrLog):
    class Meta:
        abstract = True


class Profile(AbstractUser, Log):
    nm_completo = models.CharField(max_length=200, null=True)


class Funcionario(Profile):
    cr = models.CharField(max_length=200, null=True)
    profile = models.OneToOneField(to=Profile, parent_link=True, related_name='funcionario', on_delete=models.CASCADE)


class Cliente(Profile):
    cpf = models.CharField(max_length=200, null=True)
    profile = models.OneToOneField(to=Profile, parent_link=True, related_name='cliente', on_delete=models.CASCADE)
