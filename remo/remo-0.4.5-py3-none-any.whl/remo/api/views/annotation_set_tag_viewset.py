from django.db.models import Q
from rest_framework import mixins

from remo_app.remo.models import AnnotationTags, Tag, AnnotationSet
from remo_app.remo.api.serializers import TagSerializer
from remo_app.remo.api.viewsets import BaseNestedModelViewSet


class AnnotationSetTagViewSet(mixins.ListModelMixin,
                              BaseNestedModelViewSet):
    """
    list: return project tags
    """
    parent_lookup = 'annotation_set'
    serializer_class = TagSerializer

    def get_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def get_queryset(self):
        annotation_set = self.get_parent_object_or_404()
        return AnnotationTags.objects.filter(annotation_set=annotation_set)

