from django.db import models

from remo_app.remo.api.constants import TaskType
from .tool import Tool


# TODO: drop this table
class Task(models.Model):
    name = models.CharField(max_length=255,
                            choices=TaskType.choices(),
                            default=TaskType.object_detection.value,
                            unique=True)
    type = models.CharField(max_length=255,
                            choices=TaskType.choices(),
                            default=TaskType.object_detection.name,
                            unique=True)
    available_tools = models.ManyToManyField(Tool, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        db_table = 'tasks'
