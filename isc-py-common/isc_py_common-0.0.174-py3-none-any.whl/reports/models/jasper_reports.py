import logging

from django.db.models import PositiveIntegerField

from isc_common.fields.code_field import CodeStrictField
from isc_common.models.base_ref import BaseRefHierarcy, BaseRefManager, BaseRefQuerySet

logger = logging.getLogger(__name__)


class Jasper_reportsQuerySet(BaseRefQuerySet):
    pass


class Jasper_reportsManager(BaseRefManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'code': record.code,
            'name': record.name,
            'path': record.path,
            'description': record.description,
            'username': record.username,
            'password': record.password,
            'host': record.host,
            'port': record.port,
            'parent': record.parent.id if record.parent else None
        }
        return res

    def get_queryset(self):
        return Jasper_reportsQuerySet(self.model, using=self._db)


class Jasper_reports(BaseRefHierarcy):
    path = CodeStrictField(default='/jasperserver/rest_v2/reports/')
    username = CodeStrictField(default='printer')
    password = CodeStrictField(default='printer')
    host = CodeStrictField()
    port = PositiveIntegerField()

    objects = Jasper_reportsManager()

    def __str__(self):
        return f"ID:{self.id}, code: {self.code}, name: {self.name}, path: {self.path}, description: {self.description}"

    class Meta:
        verbose_name = 'Отчеты'
