from django.db import models


# TODO: drop this table
from remo_app.remo.api.constants import ToolType


class Tool(models.Model):
    code_name = models.CharField(max_length=255,
                                 choices=ToolType.choices(),
                                 default=ToolType.rectangle.value,
                                 unique=True)

    def __str__(self):
        return self.code_name

    class Meta:
        ordering = ['id']
        db_table = 'tools'
