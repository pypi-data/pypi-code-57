from django.db.models.base import Model

from orionframework.utils.models import set_attrs


class CopyableModel(Model):
    class Meta:
        abstract = True

    def copy(self, **kwargs):
        pk = self.pk

        copy = self.__class__.objects.get(id=pk)
        copy.pk = None
        copy.id = None

        set_attrs(self, kwargs)

        copy.save(force_insert=True)

        return copy
