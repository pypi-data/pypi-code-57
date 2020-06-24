from django.db import models
from django.utils import timezone


class InteligerQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(status=True)

    def desabilitar(self, request_=None):
        usuario = request_.user if request_ is not None else None
        qs = self.update(status=False, usr_delete=usuario, dat_delete=timezone.now())
        return qs


class InteligerManager(models.Manager):
    def get_queryset(self):
        return InteligerQuerySet(self.model)

    def ativos(self):
        return self.get_queryset().ativos()

    def desabilitar(self, request_=None):
        return self.get_queryset().desabilitar(request_=request_)


class DatLog(models.Model):
    dat_insercao = models.DateTimeField(auto_now_add=True, null=True)
    dat_edicao = models.DateTimeField(auto_now=True, null=True)
    dat_delete = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class UsrLog(models.Model):
    usr_insercao = models.ForeignKey('django-inteliger.usr.Profile', on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_usr_insercao')
    usr_edicao = models.ForeignKey('django-inteliger.usr.Profile', on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_usr_edicao')
    usr_delete = models.ForeignKey('django-inteliger.usr.Profile', on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_usr_delete')

    class Meta:
        abstract = True


class Log(DatLog, UsrLog):
    objects = InteligerManager()

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

    def desabilitar(self, request_=None, *args, **kwargs):
        self.status = False
        self.usr_delete = request_.user if request_ is not None else None
        self.dat_delete = timezone.now()
        super(Log, self).save(*args, **kwargs)


class Tipo(Log):
    codigo = models.IntegerField(null=True)
    tipo = models.CharField(max_length=200, null=True)
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    class Meta:
        db_table = u'"core\".\"tipo"'
        unique_together = ('codigo', 'tipo')
