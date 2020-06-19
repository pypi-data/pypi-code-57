from django.db import models


class CategoryModelQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='publish')