from django.db import models
import core.models
from django.contrib.auth.models import AbstractUser
from compositefk.fields import CompositeForeignKey


class Profile(AbstractUser, core.models.Log):
    nm_completo = models.CharField(max_length=200, null=True)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE.TIPO')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.SET_NULL, null=True, related_name='usr_profile_tipo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta:
        #db_table = u'"core\".\"profile"'
        db_table = 'profile'