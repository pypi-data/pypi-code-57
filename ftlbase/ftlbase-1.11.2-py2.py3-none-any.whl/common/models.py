# -*- coding: utf-8 -*-

# Constantes do módulo
from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import Model, DecimalField
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel
from polymorphic.models import PolymorphicModel

from common.utils import ACAO_EDIT

ESTADOCIVIL_C = (('C', 'Casado'), ('S', 'Solteiro'), ('D', 'Divorciado'), ('', 'União Civil'))
SEXO_C = (('F', 'Feminino'), ('M', 'Masculino'))
ATIVO_C = (('S', 'Ativo'), ('I', 'Inativo'))
SIM_NAO_C = (('S', 'Sim'), ('N', 'Não'))
TIPO_DIAS_C = (('F', 'Dia Fixo'), ('C', 'Dias Corridos'), ('U', 'Dias Úteis'))


class AutoCreatedAtField(models.DateTimeField):
    """ Campo de data e hora automáticos. Para campos modified_at """

    def __init__(self, *args, **kwargs):
        # kwargs.setdefault('editable', False)
        kwargs.setdefault('default', timezone.now)
        super().__init__(*args, **kwargs)


class AutoModifiedAtField(AutoCreatedAtField):
    """ Campo de data e hora automáticos. Para campos modified_at """

    def pre_save(self, model_instance, add):
        value = timezone.now()
        if not model_instance.pk:
            for field in model_instance._meta.get_fields():
                if isinstance(field, AutoCreatedAtField) and getattr(model_instance, field.name):
                    value = getattr(model_instance, field.name)
                    break
        setattr(model_instance, self.attname, value)
        return value


class CommonAbsoluteUrlMixin(object):
    def get_absolute_url(self):
        try:
            cls_name = self._meta.model.__name__
            cls_name = cls_name[0].lower() + cls_name[1:]
            url = reverse("{}EditDelete".format(cls_name), args=(self.pk, ACAO_EDIT))
        except Exception as e:
            try:
                cls_name = self._meta.model.__name__
                cls_name = cls_name[0].lower() + cls_name[1:]
                url = reverse("{}".format(cls_name), args=(self.pk, ACAO_EDIT))
            except Exception as e:
                url = reverse('index')
        return url


class CommonModel(Model, CommonAbsoluteUrlMixin):
    """
    Usado para auditar usuário e datas de criação e modificação
    """
    # Log
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
                                   related_name='%(app_label)s_%(class)s_created_by', verbose_name='Cadastrado Por')
    created_at = AutoCreatedAtField(verbose_name='Data de Criação', blank=True, null=True)

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
                                    related_name='%(app_label)s_%(class)s_modified_by', verbose_name='Modificado Por')
    modified_at = AutoModifiedAtField(verbose_name='Última Modificação', default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = 'Auditoria de Usuário'
        verbose_name_plural = 'Auditoria de Usuários'
        abstract = True

    def __str__(self):
        return 'Criado por {} em {}, modificado por {} em {}'.format(self.created_by, self.created_at,
                                                                     self.modified_by, self.modified_at)


class CommonMPTTModel(MPTTModel, CommonModel):
    """ Common class for tree models. """

    class Meta:
        verbose_name = 'Common MPTT Model'
        verbose_name_plural = 'Common MPTT Models'
        abstract = True


class Configuracao(PolymorphicModel, CommonModel):
    """
    Configuração
    """
    apelido = models.CharField(max_length=20, null=False, blank=False, unique=True, verbose_name='Apelido', default='')
    # Status
    ativo = models.CharField(max_length=1, null=True, blank=True, verbose_name='Status', default='S',
                             choices=ATIVO_C)

    class Meta:
        verbose_name = 'Configuracao'
        verbose_name_plural = 'Configurações'
        ordering = ('apelido',)
        # abstract = True
        # managed = False

    def __str__(self):
        return u'%s' % self.apelido


class ValorField(DecimalField):

    def __init__(self, verbose_name=None, name=None, **kwargs):
        _max_digits = kwargs.pop('max_digits', 15)
        _decimal_places = kwargs.pop('decimal_places', 2)
        _blank = kwargs.pop('blank', False)
        _null = kwargs.pop('null', False)
        _default = kwargs.pop('default', 0)
        _validators = kwargs.pop('validators', [validators.MinValueValidator(0)])
        super().__init__(verbose_name=verbose_name, name=name, max_digits=_max_digits, decimal_places=_decimal_places,
                         blank=_blank, null=_null, default=_default, validators=_validators, **kwargs)


class PercentualField(ValorField):

    def __init__(self, verbose_name=None, name=None, **kwargs):
        _max_digits = kwargs.pop('max_digits', 6)
        _validators = kwargs.pop('validators', [validators.MinValueValidator(0), validators.MaxValueValidator(100)])
        super().__init__(verbose_name=verbose_name, name=name, max_digits=_max_digits, validators=_validators, **kwargs)
