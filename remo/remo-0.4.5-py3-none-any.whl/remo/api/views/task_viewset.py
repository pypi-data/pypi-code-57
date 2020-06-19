from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter

from remo_app.remo.api.serializers import TaskSerializer
from remo_app.remo.models import Task


class TaskFilterSet(FilterSet):
    autocomplete = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Task
        fields = ('autocomplete', )


class TaskViewSet(ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = TaskFilterSet
    ordering = 'name'
