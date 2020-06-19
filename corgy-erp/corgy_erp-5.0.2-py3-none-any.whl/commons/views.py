from material.frontend.views import ModelViewSet

from . import models

class PersonModelViewSet(ModelViewSet):
    model = models.Person
    list_display = [
        'id',
        'full_name'
    ]

