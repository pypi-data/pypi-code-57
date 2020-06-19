from django.db import models
from djangopost.querysets import CategoryModelQuerySet


class CategoryModelManager(models.Manager):
    def get_queryset(self):
        return CategoryModelQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()