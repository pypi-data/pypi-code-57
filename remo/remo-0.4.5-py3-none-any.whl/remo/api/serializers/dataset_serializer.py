import logging

from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from remo_app.remo.api.serializers import LicenseSerializer
from remo_app.remo.models import DatasetImage, Dataset, ImageFolder, AnnotationObject, DatasetStatistics

logger = logging.getLogger('remo_app')

MAXIMUM_THUMBNAILS_COUNT = 4


class DatasetSerializer(serializers.ModelSerializer):
    license = LicenseSerializer(read_only=True)
    top3_classes = serializers.SerializerMethodField()
    total_classes = serializers.SerializerMethodField()
    total_annotation_objects = serializers.SerializerMethodField()
    is_readonly = SerializerMethodField()

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)

    def get_top3_classes(self, instance):
        stats = DatasetStatistics.objects.filter(dataset=instance).first()
        if not stats:
            return []
        return stats.statistics.get('top3_classes', [])

    def get_total_classes(self, instance):
        stats = DatasetStatistics.objects.filter(dataset=instance).first()
        if not stats:
            return 0
        return stats.statistics.get('total_classes', 0)

    def get_total_annotation_objects(self, instance):
        images = instance.dataset_images.all()
        return AnnotationObject.objects.filter(annotation__image__in=images).count()

    def get_is_readonly(self, instance):
        user = self.context['request'].user
        if user == instance.user:
            return False
        # TODO: check later in instance.users_shared
        return True

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'annotation_sets', 'created_at', 'license', 'is_public', 'is_readonly',
                  'users_shared', 'top3_classes', 'total_classes', 'total_annotation_objects')
        read_only_fields = ('created_at', 'is_public', 'users_shared', 'annotation_sets')


class UserDatasetSerializer(DatasetSerializer):
    image_thumbnails = SerializerMethodField()
    owner = SerializerMethodField()

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)

    def get_image_thumbnails(self, obj):
        """ Return list of images links """
        queryset = obj.dataset_images.all()
        return [img.image_object.preview.url for img in queryset[:MAXIMUM_THUMBNAILS_COUNT]]

    def get_owner(self, obj):
        result = ''
        if obj.user:
            result = obj.user.get_full_name().strip()
        return result if result else 'Unknown'

    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'owner', 'is_archived', 'image_thumbnails', 'quantity', 'size_in_bytes',
            'created_at', 'updated_at', 'license', 'is_public', 'is_readonly', 'users_shared', 'top3_classes',
            'total_classes'
        )
        read_only_fields = ('created_at', 'updated_at', 'is_public', 'users_shared')


class DatasetImageDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'created_at', 'is_public')


class ListDatasetSerializer(UserDatasetSerializer):
    image_thumbnails = SerializerMethodField()

    # TODO: check for image optimization
    def get_image_thumbnails(self, obj):
        """ Return list of images full data """
        from remo_app.remo.api.serializers import DatasetImageSerializer
        queryset = obj.dataset_images.all()
        # count_of_images_returned = min(MAXIMUM_THUMBNAILS_COUNT, dataset_images_queryset.count())

        return [DatasetImageSerializer(img, context=self.context).data
                for img in queryset[:MAXIMUM_THUMBNAILS_COUNT]]

    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'image_thumbnails', 'quantity', 'size_in_bytes', 'created_at',
            'license', 'is_public', 'users_shared', 'top3_classes', 'total_classes'
        )
        read_only_fields = ('created_at', 'is_public', 'users_shared')


class UserDatasetContentsSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        return self._get_instance_type(instance)

    def get_image(self, instance):
        from remo_app.remo.api.serializers.image_serializer import DatasetImageAnnotationsSerializer
        if self._get_instance_type(instance) != 'image':
            return None

        return DatasetImageAnnotationsSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        from remo_app.remo.api.serializers.folder_serializer import \
            BriefUserDatasetFolderSerializer
        if self._get_instance_type(instance) != 'folder':
            return None

        return BriefUserDatasetFolderSerializer(instance, context=self.context).data

    def _get_instance_type(self, instance):
        types = {
            ImageFolder: 'folder',
            DatasetImage: 'image'
        }
        return types.get(type(instance))
