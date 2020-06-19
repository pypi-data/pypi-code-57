import logging
# import coreapi
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import mixins, viewsets
# from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response

from remo_app.remo.api.views.mixins import UpdateDatasetModelMixin, DestroyDatasetModelMixin
from remo_app.remo.api.serializers import (
    UserDatasetSerializer,
    DatasetUserImageSerializer,
)
from remo_app.remo.models import Dataset

logger = logging.getLogger('remo_app')


# class LastViewFilterBackend(BaseFilterBackend):
#     last_view = 'last_view'
#
#     def filter_queryset(self, request, queryset, view):
#         last_view = request.query_params.get('last_view')
#         if not last_view:
#             return queryset
#         return queryset.filter(last_view__isnull=False).order_by('-last_view__last_view')
#
#     def get_schema_fields(self, view):
#         return [
#             coreapi.Field(name=self.last_view, required=False, location='query'),
#         ]


class UserDatasetViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         DestroyDatasetModelMixin,
                         UpdateDatasetModelMixin,
                         viewsets.GenericViewSet):
    # filter_backends = (LastViewFilterBackend, DjangoFilterBackend)
    filter_backends = (DjangoFilterBackend,)
    serializer_class = UserDatasetSerializer
    queryset = Dataset.objects.all()
    filter_fields = ('is_archived', 'is_public')

    serializer_action_classes = {
        'retrieve': UserDatasetSerializer,
        'image': DatasetUserImageSerializer,
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(user=self.request.user) | Q(is_public=True))

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    @action(['get'], detail=True, url_path='image')
    def image(self, request, pk=None):
        queryset = self.get_object().dataset_images.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
