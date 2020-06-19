from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        db_table = 'classes'

    def __str__(self):
        return self.name
