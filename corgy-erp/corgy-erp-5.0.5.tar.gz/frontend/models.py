from django.db import models

# Create your models here.

# class MyModel(models.Model):
#     name = models.CharField(max_length=250)


class Profile(models.Model):
    class Meta:
        db_table = 'profiles'
        verbose_name = _("profil")
        verbose_name_plural = _("profilok")