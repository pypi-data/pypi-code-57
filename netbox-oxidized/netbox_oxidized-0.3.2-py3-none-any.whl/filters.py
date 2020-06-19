import django_filters
from django.db.models import Q
from utilities.filters import BaseFilterSet
from .models import OxidizedNode

class OxidizedNodeFilterSet(BaseFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )


    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(node_model__icontains=value) |
            Q(group__icontains=value)
        )

    class Meta():
        model = OxidizedNode
        fields = ['name', 'node_model','group']
