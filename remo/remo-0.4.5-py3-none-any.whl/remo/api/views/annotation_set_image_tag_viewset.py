from django.db.models import Q
from rest_framework import mixins

from remo_app.remo.models import AnnotationSet, DatasetImage, Tag
from remo_app.remo.api.serializers import (
    AnnotationSetImageTagSerializer
)
from remo_app.remo.api.viewsets import BaseGrandNestedModelViewSet


class AnnotationSetImageTagViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   BaseGrandNestedModelViewSet):
    grand_parent_lookup = 'annotation_set'
    parent_lookup = 'image'
    serializer_class = AnnotationSetImageTagSerializer

    def destroy(self, request, *args, **kwargs):
        dataset_image = self.get_parent_object_or_404()
        dataset_image.dataset.update()
        return super().destroy(request, *args, **kwargs)

    def get_grand_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def get_parent_queryset(self):
        annotation_set = self.get_grand_parent_object_or_404()
        return DatasetImage.objects.filter(dataset=annotation_set.dataset)

    def get_queryset(self):
        dataset_image = self.get_parent_object_or_404()
        annotation_set = self.get_grand_parent_object_or_404()
        return Tag.objects.filter(image=dataset_image, annotation_set=annotation_set)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['dataset_image'] = self.get_parent_object_or_404()
        ctx['annotation_set'] = self.get_grand_parent_object_or_404()
        return ctx
