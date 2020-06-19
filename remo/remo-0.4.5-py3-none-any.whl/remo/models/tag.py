from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name
