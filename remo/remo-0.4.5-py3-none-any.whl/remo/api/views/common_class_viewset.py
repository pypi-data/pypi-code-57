from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter

from remo_app.remo.api.serializers import CommonClassSerializer
from remo_app.remo.models import Class
from remo_app.remo.use_cases.classes import capitalize_class_name


class CommonClassFilterSet(FilterSet):
    autocomplete = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Class
        fields = ('autocomplete', )


class CommonClassViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Class.objects.all()
    serializer_class = CommonClassSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CommonClassFilterSet
    ordering = 'name'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_name = serializer.validated_data['name'].lower()
        class_name = capitalize_class_name(class_name)
        serializer.validated_data['name'] = class_name

        exist_class = self.queryset.filter(name=class_name).first()
        if exist_class is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        serializer = self.get_serializer(exist_class)
        return Response(serializer.data, status=status.HTTP_200_OK)
