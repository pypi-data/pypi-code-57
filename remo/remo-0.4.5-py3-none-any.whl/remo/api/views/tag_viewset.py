from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from remo_app.remo.models import AnnotationTags, Tag
from remo_app.remo.api.serializers import TagAutocompleteSerializer


class TagFilterSet(FilterSet):
    autocomplete = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Tag
        fields = ('autocomplete',)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TagAutocompleteSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = TagFilterSet
    ordering = 'name'

    def get_queryset(self):
        return Tag.objects.filter(
            pk__in=AnnotationTags.objects.filter(
                annotation_set__user=self.request.user
            ).values_list(
                'tag__id', flat=True
            ).distinct()
        )

    def list(self, request, *args, **kwargs):
        if 'autocomplete' not in self.request.query_params:
            return Response({
                'error': True,
                'detail': "'autocomplete' query parameter is required",
                'next': None,
                'previous': None,
                'results': [],
                'count': 0
            }, status=400)

        return super().list(request, *args, **kwargs)
