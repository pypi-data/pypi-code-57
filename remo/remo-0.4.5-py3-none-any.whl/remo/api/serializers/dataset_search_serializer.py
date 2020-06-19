from rest_framework import serializers

from remo_app.remo.models import Dataset, ImageFolder

from remo_app.remo.api.serializers import (
    DatasetSerializer,
    BriefUserDatasetFolderSerializer
)


class DatasetSearchSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    dataset = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        types = {
            ImageFolder: 'folder',
            Dataset: 'dataset'
        }
        return types.get(type(instance))

    def get_dataset(self, instance):
        if type(instance) != Dataset:
            return None

        return DatasetSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        if type(instance) != ImageFolder:
            return None

        return BriefUserDatasetFolderSerializer(instance, context=self.context).data
