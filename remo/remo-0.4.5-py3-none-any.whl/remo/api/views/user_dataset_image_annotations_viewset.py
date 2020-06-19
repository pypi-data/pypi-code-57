import logging

from django.db.models import Q
from rest_framework import mixins

from remo_app.remo.api.serializers.image_serializer import DatasetImageAnnotationsSerializer
from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import Dataset, DatasetImage

logger = logging.getLogger('remo_app')


class UserDatasetImageAnnotationsViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              BaseNestedModelViewSet):
    parent_lookup = 'user_dataset'
    serializer_class = DatasetImageAnnotationsSerializer

    def get_parent_queryset(self):
        return Dataset.objects.filter(
            Q(user=self.request.user) | Q(is_public=True),
            is_archived=False
        )

    def get_queryset(self):
        return DatasetImage.objects.filter(
            dataset=self.parent_pk,
        )
