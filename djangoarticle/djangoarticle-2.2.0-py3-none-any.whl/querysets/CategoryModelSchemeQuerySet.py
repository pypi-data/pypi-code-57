from django.db import models 


class CategoryModelSchemeQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='publish')