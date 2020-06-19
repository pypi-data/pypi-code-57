from rest_framework import serializers

from remo_app.remo.api.serializers.image_serializer import DatasetUserImageSerializer
from remo_app.remo.models import ImageFolder

from remo_app.remo.models.folder import ImageFolderStatistics


class BriefUserDatasetFolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    dataset_id = serializers.IntegerField(source='dataset.id', read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    preview = serializers.SerializerMethodField()
    total_images = serializers.SerializerMethodField()
    top3_classes = serializers.SerializerMethodField()
    total_classes = serializers.SerializerMethodField()

    def get_preview(self, instance):
        img = instance.contents.first()
        if img:
            return img.image_object.preview.url if img.image_object.preview else None

        return None

    def get_total_images(self, instance):
        return instance.contents.count()

    def get_top3_classes(self, instance):
        stats = ImageFolderStatistics.objects.filter(image_folder=instance).first()
        if not stats:
            return []
        return stats.statistics.get('top3_classes', [])

    def get_total_classes(self, instance):
        stats = ImageFolderStatistics.objects.filter(image_folder=instance).first()
        if not stats:
            return 0
        return stats.statistics.get('total_classes', 0)

    class Meta:
        model = ImageFolder
        fields = ('id', 'name', 'dataset_id', 'updated_at', 'created_at', 'preview',
                  'total_images', 'top3_classes', 'total_classes')


class DetailUserDatasetFolderSerializer(BriefUserDatasetFolderSerializer):
    contents = DatasetUserImageSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, instance):
        img = instance.contents.first()
        return img.image_object.thumbnail.url if img and img.image_object.thumbnail else None

    class Meta:
        model = ImageFolder
        fields = ('id', 'name', 'dataset_id', 'updated_at', 'created_at', 'contents', 'thumbnail')
