import logging

from django.db.models import Q
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from queryset_sequence import QuerySetSequence


from remo_app.remo.api.serializers import UserDatasetContentsSerializer
from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import ImageFolder, DatasetImage, Dataset

logger = logging.getLogger('remo_app')

class UserDatasetContentsViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 BaseNestedModelViewSet):
    parent_lookup = 'user_dataset'
    serializer_class = UserDatasetContentsSerializer

    def get_parent_queryset(self):
        return Dataset.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def get_contents(self, folder_object=None):
        """
        Return contents of dataset folder
        :param folder_object: folder to list contents of, Default: root
        :return: Response object with paginated results
        """
        folders = ImageFolder.objects.filter(
            Q(dataset__user=self.request.user) | Q(dataset__is_public=True),
            dataset=self.parent_pk
        )
        images = DatasetImage.objects.filter(
            Q(dataset__user=self.request.user) | Q(dataset__is_public=True),
            dataset=self.parent_pk
        )

        if folder_object:
            images = images.filter(folder=folder_object)
        else:
            images = images.filter(folder__isnull=True)
        folders = folders.filter(parent=folder_object)

        queryset = QuerySetSequence(folders, images)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return self.get_contents(folder_object=None)

    def retrieve(self, request, *args, **kwargs):
        # TODO: make walk contents/folder1/folder2/..., #333
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        fltr = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(ImageFolder, **fltr)

        return self.get_contents(obj)
