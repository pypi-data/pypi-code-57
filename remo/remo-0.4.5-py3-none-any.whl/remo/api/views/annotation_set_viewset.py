from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from remo_app.remo.models import AnnotationSet
from remo_app.remo.api.serializers import (
    AnnotationSetLastAnnotatedSerializer,
    AnnotationSetSerializer,
    AnnotationSetModifySerializer
)


class AnnotationSetViewset(ModelViewSet):
    ordering = 'pk'
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return AnnotationSetSerializer
        return AnnotationSetModifySerializer

    def get_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    @action(['get'], detail=True, url_path='export')
    def export(self, request, *args, **kwargs):
        format = request.query_params.get('dumpFormat', 'json')
        data = request.query_params.get('data', '[]')

        path = 'dump.{}'.format(format)
        file = open('{}/{}'.format(settings.MEDIA_ROOT, path), 'w')
        file.write(data)
        file.close()

        return Response({'link': '{}{}'.format(settings.MEDIA_URL, path)})

    @action(methods=['get'], detail=True, url_path='last-annotated')
    def last_annotated(self, request, pk=None):
        # TODO: deprecated?
        serializer = AnnotationSetLastAnnotatedSerializer
        return Response(serializer(self.get_object()).data)
