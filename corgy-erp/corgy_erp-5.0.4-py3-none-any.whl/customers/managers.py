from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging

class CustomerQuerySet(models.QuerySet):

    def organizations(self):
        return self.filter(classification='organization')

    def individuals(self):
        return self.filter(classification='individual')

class CustomerManager(models.Manager):

    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def individuals(self):
        return self.get_queryset().individuals()

    def organizations(self):
        return self.get_queryset().organizations()

    def create_organization(self, **kwargs):
        entity = super().create(**kwargs)
        kwargs['classification'] = 'organization'
        logging.debug(_('Új társas vállalkozás {name} létrehozva'.format(name=str(entity))))
        return entity

    def create_individual(self, **kwargs):
        kwargs['classification'] = 'individual'
        entity = super().create(**kwargs)
        logging.debug(_('Új egyéni vállalkozás {name} létrehozva'.format(name=str(entity))))
        return entity