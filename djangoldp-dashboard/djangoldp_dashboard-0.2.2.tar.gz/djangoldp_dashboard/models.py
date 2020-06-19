from django.db import models
from djangoldp.models import Model

SIZE_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
]

class Dashboard(Model):
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='1')
    content = models.TextField()
