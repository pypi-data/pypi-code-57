from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from remo_app.remo.api.constants import AnnotationSetType


class AnnotationSetTypeViewSet(ViewSet):
    def list(self, request, *args, **kwargs):
        return Response([{'id': key, 'name': value}
                         for key, value in AnnotationSetType.choices()])
