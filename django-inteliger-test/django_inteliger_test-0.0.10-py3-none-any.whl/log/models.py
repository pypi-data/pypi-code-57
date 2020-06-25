from django.db import models
import core.models


class Log(core.models.Log):
    status_code = models.IntegerField(null=True)
    reason_phrase = models.CharField(max_length=500, null=True)
    metodo = models.CharField(max_length=30, null=True)
    ip = models.GenericIPAddressField(null=True)
    path = models.CharField(max_length=500, null=True)
    session_id = models.CharField(max_length=200, null=True)

    class Meta:
        #db_table = u'"log\".\"log"'
        db_table = 'log'