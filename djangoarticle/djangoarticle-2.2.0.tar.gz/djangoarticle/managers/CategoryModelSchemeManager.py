from django.db import models
from djangoarticle.querysets import CategoryModelSchemeQuerySet


class CategoryModelSchemeManager(models.Manager):
    def get_queryset(self):
        return CategoryModelSchemeQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()