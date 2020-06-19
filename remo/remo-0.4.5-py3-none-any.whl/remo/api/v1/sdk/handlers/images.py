from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from remo_app.remo.api.v1.sdk.handlers.serializers import DatasetImageSerializer
from remo_app.remo.models import DatasetImage


class Images(GenericViewSet):
    serializer_class = DatasetImageSerializer

    def retrieve(self, request, pk=None):
        img = DatasetImage.objects.filter(id=pk).first()
        if not img:
            return Response({'error': 'Image with id: {}, was not found.'.format(pk)}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()(img)
        return Response(serializer.data)
