from django.db import models
from djangoarticle.querysets import ArticleModelSchemeQuerySet


class ArticleModelSchemeManager(models.Manager):
    def get_queryset(self):
        return ArticleModelSchemeQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def promoted(self):
        return self.get_queryset().promoted()

    def trending(self):
        return self.get_queryset().trending()

    def author(self, username):
        return self.get_queryset().author(username)

    def promotional(self):
        return self.get_queryset().promotional()

    def opinion(self):
        return self.get_queryset().opinion()