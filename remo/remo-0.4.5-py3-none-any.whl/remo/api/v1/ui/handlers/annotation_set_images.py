from django.db.models import Q
from rest_framework import mixins

from remo_app.remo.models import AnnotationSet, DatasetImage
from remo_app.remo.api.serializers import AnnotationSetImageSerializer
from remo_app.remo.api.viewsets import BaseNestedModelViewSet


class AnnotationSetImages(mixins.ListModelMixin,
                                BaseNestedModelViewSet):
    parent_lookup = 'annotation_sets'
    serializer_class = AnnotationSetImageSerializer

    def get_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'annotation_set': self.get_parent_object_or_404()
        }

    def get_queryset(self):
        annotation_set = self.get_parent_object_or_404()
        return DatasetImage.objects.filter(dataset=annotation_set.dataset)
