from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied

from remo_app.remo.api.serializers import (
    BriefUserDatasetFolderSerializer,
    DetailUserDatasetFolderSerializer
)
from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import ImageFolder, Dataset


class UserDatasetFolderViewSet(mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               BaseNestedModelViewSet):
    filter_backends = (DjangoFilterBackend, )
    parent_lookup = 'user_dataset'

    def get_serializer_class(self):
        if self.action == 'list':
            return BriefUserDatasetFolderSerializer
        return DetailUserDatasetFolderSerializer

    def get_parent_queryset(self):
        return Dataset.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        ).filter(is_archived=False)

    def get_queryset(self):
        # TODO: restrict to team when it will be implemented, #272
        dataset = self.get_parent_object_or_404()
        return ImageFolder.objects.filter(dataset=dataset).order_by('id')

    def create(self, request, *args, **kwargs):
        dataset = self.get_dataset_or_403(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['dataset'] = dataset

        parent_folder_id = request.data.get('parent_folder_id')
        if parent_folder_id:
            parent = ImageFolder.objects.filter(id=parent_folder_id).first()
            if parent:
                data['parent'] = parent

        obj = ImageFolder.objects.create(**data)

        serializer = self.get_serializer(obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        dataset = self.get_dataset_or_403(request)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['dataset'] = dataset
        for k, v in data.items():
            setattr(instance, k, v)
        instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        dataset = self.get_dataset_or_403(request)

        return super().destroy(request, *args, **kwargs)

    def get_dataset_or_403(self, request):
        dataset = Dataset.objects.get(pk=self.parent_pk)
        if dataset.is_public and not request.user.is_superuser:
            raise PermissionDenied

        return dataset
