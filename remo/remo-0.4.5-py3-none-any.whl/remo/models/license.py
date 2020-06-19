from django.db import models


class License(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'licenses'

    def __str__(self):
        return self.name
