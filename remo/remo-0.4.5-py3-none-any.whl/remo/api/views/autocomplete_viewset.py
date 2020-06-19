from django.db.models import Q
from queryset_sequence import QuerySetSequence
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin

from remo_app.remo.models import AnnotationTags, Tag, ImageFolder, Dataset, Class, Task, AnnotationSet
from remo_app.remo.api.serializers import AutocompleteSerializer, AutocompleteQuerySerializer


class AutocompleteViewSet(GenericViewSet, ListModelMixin):
    serializer_class = AutocompleteSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsed_query = {}

    def get_queryset(self):
        query = self.parsed_query["query"].value

        classes_ids = AnnotationSet.objects.filter(Q(dataset__is_public=True) | Q(user=self.request.user)).values(
            "classes")
        tag_ids = AnnotationTags.objects.filter(
            Q(annotation_set__dataset__is_public=True) | Q(annotation_set__user=self.request.user)).values("tag")

        query_sets = (
            Task.objects.filter(annotation_sets__user=self.request.user,
                                name__icontains=query).order_by("name").distinct(),
            Dataset.objects.filter(Q(is_public=True) | Q(user=self.request.user),
                                   name__icontains=query).order_by("name").distinct(),
            Tag.objects.filter(id__in=tag_ids, name__icontains=query).order_by("name").distinct(),
            ImageFolder.objects.filter(Q(dataset__is_public=True) | Q(dataset__user=self.request.user),
                                       name__icontains=query).distinct(),
            Class.objects.filter(id__in=classes_ids, name__icontains=query)
        )

        return QuerySetSequence(*query_sets)

    def list(self, request):
        self.parsed_query = parsed_query = AutocompleteQuerySerializer(data=request.query_params)

        if not parsed_query.is_valid():
            return Response({"fields": parsed_query.errors, "error": True}, status=400)

        return super().list(request)
