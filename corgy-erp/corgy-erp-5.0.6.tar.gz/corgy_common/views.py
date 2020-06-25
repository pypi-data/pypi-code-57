from material.frontend.views import ModelViewSet
from django.views.generic import View
from commons.models import Person
from . import models

class PersonModelViewSet(ModelViewSet):
    model = Person

class SinglePageApplicationView(View):
    pass