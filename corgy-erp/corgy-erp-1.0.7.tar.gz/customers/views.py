from material.frontend.views import ModelViewSet
from .models import Customer
from .models import Organization
from .models import Individual

class CustomerModelViewSet(ModelViewSet):
    model = Customer
    list_display = [
        'id',
        'name'
    ]

class OrganizationModelViewSet(ModelViewSet):
    model = Organization

class IndividualModelViewSet(ModelViewSet):
    model = Individual
