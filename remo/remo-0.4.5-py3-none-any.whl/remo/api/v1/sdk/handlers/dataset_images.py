from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from remo_app.remo.api.v1.sdk.handlers.serializers import DatasetImageSerializer
from remo_app.remo.models import DatasetImage, Dataset


class DatasetImages(GenericViewSet):
    serializer_class = DatasetImageSerializer

    @action(["get"], detail=True, url_path="images")
    def images(self, request, pk=None):
        dataset = Dataset.objects.filter(id=pk).first()
        if not dataset:
            return Response(
                {"error": "Dataset with id: {}, was not found.".format(pk)},
                status=status.HTTP_404_NOT_FOUND,
            )

        images = DatasetImage.objects.filter(dataset=dataset)

        has_limit = request.query_params.get("limit")
        if has_limit:
            page = self.paginate_queryset(images)
            if page:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(images, many=True)
        return Response({"count": images.count(), "results": serializer.data})
