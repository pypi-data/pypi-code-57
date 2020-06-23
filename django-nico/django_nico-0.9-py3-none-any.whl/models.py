from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class DatLog(models.Model):
    dat_insercao = models.DateTimeField(auto_now_add=True, null=True)
    dat_edicao = models.DateTimeField(auto_now=True, null=True)
    dat_delete = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class UsrLog(models.Model):
    usr_insercao = models.ForeignKey('nico.Profile', on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_usr_insercao')
    usr_edicao = models.ForeignKey('nico.Profile', on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_usr_edicao')
    usr_delete = models.ForeignKey('nico.Profile', on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_usr_delete')

    class Meta:
        abstract = True


class Log(DatLog, UsrLog):
    status = models.BooleanField(null=True, default=True)
    class Meta:
        abstract = True

    def save(self, request_=None, *args, **kwargs):
        if request_ is not None:
            if self.pk is None:
                self.usr_insercao = request_.user if request_ is not None else None
                self.dat_insercao = timezone.now()
                self.status = True
            else:
                self.usr_edicao = request_.user if request_ is not None else None
                self.dat_edicao = timezone.now()
        super(Log, self).save(*args, **kwargs)

    def disable(self, request_=None, *args, **kwargs):
        self.status = False
        self.usr_delete = request_.user if request_ is not None else None
        self.dat_delete = timezone.now()
        super(Log, self).save(*args, **kwargs)


class Profile(AbstractUser, Log):
    nm_completo = models.CharField(max_length=200, null=True)


class Funcionario(Profile):
    cr = models.CharField(max_length=200, null=True)
    profile = models.OneToOneField(to=Profile, parent_link=True, related_name='funcionario', on_delete=models.CASCADE)


class Cliente(Profile):
    cpf = models.CharField(max_length=200, null=True)
    profile = models.OneToOneField(to=Profile, parent_link=True, related_name='cliente', on_delete=models.CASCADE)
