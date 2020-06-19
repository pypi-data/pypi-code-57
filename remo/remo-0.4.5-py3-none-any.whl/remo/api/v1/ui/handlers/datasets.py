import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from django.db.models import Q
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response

from remo_app.remo.models import Dataset, DatasetStatistics, DatasetImage

MAXIMUM_THUMBNAILS_COUNT = 4

logger = logging.getLogger('remo_app')


class DatasetSerializer(serializers.ModelSerializer):
    image_thumbnails = SerializerMethodField()
    owner = SerializerMethodField()
    is_readonly = SerializerMethodField()
    quantity = SerializerMethodField()

    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'owner', 'is_archived', 'image_thumbnails', 'quantity', 'size_in_bytes',
            'created_at', 'updated_at', 'license', 'is_public', 'is_readonly'
        )

    def get_quantity(self, obj):
        return DatasetImage.objects.filter(dataset=obj).count()

    def get_image_thumbnails(self, obj):
        queryset = obj.dataset_images.all()
        return [img.image_object.preview.url for img in queryset[:MAXIMUM_THUMBNAILS_COUNT]]

    def get_owner(self, obj):
        result = ''
        if obj.user:
            result = obj.user.get_full_name().strip()
        return result if result else 'Unknown'

    def get_is_readonly(self, instance):
        user = self.context['request'].user
        if user == instance.user:
            return False
        # TODO: check later in instance.users_shared
        return True


class DatasetDetailsSerializer(DatasetSerializer):
    top3_classes = SerializerMethodField()
    total_classes = SerializerMethodField()

    class Meta:
        model = Dataset
        fields = (
            'id', 'name', 'owner', 'is_archived', 'image_thumbnails', 'quantity', 'size_in_bytes',
            'created_at', 'updated_at', 'license', 'is_public', 'users_shared', 'top3_classes',
            'total_classes', 'is_readonly'
        )

    def get_top3_classes(self, instance):
        stats = DatasetStatistics.objects.filter(dataset=instance).first()
        if not stats or not stats.statistics:
            return []
        return stats.statistics.get('top3_classes', [])

    def get_total_classes(self, instance):
        stats = DatasetStatistics.objects.filter(dataset=instance).first()
        if not stats or not stats.statistics:
            return 0
        return stats.statistics.get('total_classes', 0)


class Datasets(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    filter_backends = (DjangoFilterBackend,)
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()
    filter_fields = ('is_archived', 'is_public')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(user=self.request.user) | Q(is_public=True))

    @action(['get'], detail=True, url_path='details')
    def details(self, request, pk=None):
        dataset = self.get_queryset().get(id=pk)
        return Response(DatasetDetailsSerializer(dataset, context={'request': request}).data)
