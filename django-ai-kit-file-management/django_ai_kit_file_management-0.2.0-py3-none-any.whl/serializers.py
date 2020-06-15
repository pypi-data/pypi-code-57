from rest_framework.serializers import ModelSerializer
from .settings import api_settings


class FileSerializer(ModelSerializer):
    class Meta:
        model = api_settings.FILE_MODEL
        fields = ["id", "file", "creator", "format", "name"]
