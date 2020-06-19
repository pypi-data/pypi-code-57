from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from rest_framework import mixins

from remo_app.remo.models import AnnotationSet, Dataset
from remo_app.remo.api.serializers import DatasetAnnotationSetSerializer
from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.api.shortcuts import can_user_modify_dataset


class DatasetAnnotationSetViewSet(mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin,
                                  BaseNestedModelViewSet):
    parent_lookup = 'dataset'
    filter_backends = (DjangoFilterBackend,)
    serializer_class = DatasetAnnotationSetSerializer

    def get_parent_queryset(self):
        return Dataset.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        ).filter(is_archived=False)

    def get_queryset(self):
        # TODO: restrict to team when it will be implemented, #272
        dataset = self.get_parent_object_or_404()
        return AnnotationSet.objects.filter(dataset=dataset)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['dataset'] = self.get_parent_object_or_404()
        return ctx

    def perform_destroy(self, instance):
        if not can_user_modify_dataset(self.request.user, instance.dataset):
            raise PermissionDenied

        return super().perform_destroy(instance)
