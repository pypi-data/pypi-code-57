import os
from django.core.exceptions import (
    ValidationError as DjangoValidatonError,
    ImproperlyConfigured,
)
from django.conf import settings
from django.http import FileResponse

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .settings import api_settings

FILE_MODEL = api_settings.FILE_MODEL
SERIALIZER = api_settings.SERIALIZER


class FileViewSet(ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing file instances.
    """

    serializer_class = SERIALIZER

    def get_queryset(self):
        return FILE_MODEL.objects.visible_for(self.request.user)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        """
        we use this method instead of the permission_classes attribute because
        we have to monkey patch the api_settings for tests
        """
        return [permission() for permission in api_settings.PERMISSION_CLASSES]

    def post(self, request, format=None):
        file = request.data["file"]
        serializer = SERIALIZER(
            data={
                "file": file,
                "creator": request.user.pk if request.user.is_authenticated else None,
            }
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)
        except ValidationError as e:
            # we have to rewrite some error codes to make them clearer
            errors = e.get_codes()
            file_errors = errors.get("file")

            def rewrite(name):
                if name == "max_length":
                    return "filename_too_long"

            if file_errors:
                errors["file"] = [rewrite(error) for error in file_errors]
            raise ValidationError(errors)
        except DjangoValidatonError as e:
            raise ValidationError({"file": e.messages})


class FileDownloadView(APIView):
    def get(self, request, uuid, filename):
        try:
            identifier = os.path.join(uuid, filename)
            file_obj = FILE_MODEL.objects.visible_for(request.user).get(file=identifier)
            file_name_on_disk = file_obj.file.name
            backend = api_settings.FILESERVER_BACKEND
            if backend == "dev":
                return FileResponse(
                    open(os.path.join(settings.MEDIA_ROOT, file_name_on_disk), "rb"),
                    filename=file_obj.name,
                    as_attachment=True,
                    content_type=file_obj.format,
                )

            response = FileResponse(
                b"",
                filename=file_obj.name,
                as_attachment=True,
                content_type=file_obj.format,
            )
            response[
                {"nginx": "X-Accel-Redirect", "x-sendfile": "X-Sendfile"}[backend]
            ] = os.path.join(settings.MEDIA_ROOT, file_name_on_disk).encode("utf-8")
            return response

        except AttributeError:
            raise ImproperlyConfigured(
                "Manager for File Model is missing the 'visible_for' method"
            )
