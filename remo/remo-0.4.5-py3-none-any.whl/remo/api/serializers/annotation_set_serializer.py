from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count
from rest_framework import serializers

from remo_app.remo.models import AnnotationSet, AnnotationClassRel, AnnotationObject
from remo_app.remo.models.annotation_set import AnnotationSetStatistics
from remo_app.remo.api.serializers import (
    CommonClassSerializer,
    TaskSerializer,
    UserDatasetSerializer,
    CommonClassNestedSerializer
)
from remo_app.remo.api.shortcuts import can_user_modify_dataset, can_user_modify_annotation_set
from remo_app.remo.models import Task, Dataset, Class, DatasetImage
from remo_app.remo.stores.image_store import ImageStore


class AnnotationSetSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=False)
    classes = CommonClassSerializer(many=True, required=False)
    dataset = UserDatasetSerializer(many=False, required=False)
    images_without_annotations = serializers.SerializerMethodField()
    is_last_modified = serializers.SerializerMethodField()
    is_public = serializers.SerializerMethodField()

    def get_is_last_modified(self, obj):
        # TODO: probably obsolete
        return False

    def get_images_without_annotations(self, instance):
        return ImageStore.calc_images_without_annotations(instance.id)

    def get_is_public(self, instance):
        return instance.dataset.is_public

    class Meta:
        model = AnnotationSet
        fields = ('id', 'name', 'released_at', 'updated_at', 'task', 'dataset',
                  'last_annotated_date', 'classes', 'is_last_modified', 'type',
                  'is_public', 'images_without_annotations')


class AnnotationSetModifySerializer(AnnotationSetSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=True)
    classes = CommonClassNestedSerializer(many=True, required=False)
    dataset = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all(), required=True)

    def validate_dataset(self, data):
        user = self.context['request'].user
        if not user.is_superuser and data.is_public:
            raise ValidationError('Public dataset "{}" is read-only'.format(data.pk))
        if data.user != user:
            raise ValidationError('Invalid pk "{}" - object does not exist.'.format(data.pk))

        return data

    def validate(self, attrs):
        user = self.context['request'].user
        if self.instance and not can_user_modify_annotation_set(user, self.instance):
            raise ValidationError(
                'Public annotation set "{}" is read-only'.format(self.instance.pk)
            )

        return attrs

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user

        with transaction.atomic():
            classes_data = validated_data.pop('classes', None)
            instance = super().update(instance, validated_data)
            if classes_data is not None:
                self._set_classes(instance, classes_data)

        return instance

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        with transaction.atomic():
            classes_data = validated_data.pop('classes', None)
            instance = super().create(validated_data)
            if classes_data is not None:
                self._set_classes(instance, classes_data)

        return instance

    def _set_classes(self, instance, class_data):
        class_names = [cl['name'] for cl in class_data]
        instance.classes.set(list(Class.objects.filter(name__in=class_names)))

    class Meta:
        model = AnnotationSet
        fields = ('id', 'name', 'released_at', 'updated_at', 'task', 'dataset',
                  'last_annotated_date', 'classes', 'is_last_modified', 'type',
                  'is_public')
        read_only_fields = ('id', 'updated_at', 'last_annotated_date', 'user')


class DatasetAnnotationSetSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    updated_at = serializers.DateTimeField(read_only=True)
    task = TaskSerializer()
    annotated_images_count = serializers.SerializerMethodField()
    total_images = serializers.IntegerField(source='dataset.quantity', read_only=True)
    top3_classes = serializers.SerializerMethodField()
    total_classes = serializers.SerializerMethodField()
    total_annotation_objects = serializers.SerializerMethodField()
    is_public = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    def get_annotated_images_count(self, instance):
        return instance.annotations.filter(image__isnull=False).count()

    def get_top3_classes(self, instance):
        stats = AnnotationSetStatistics.objects.filter(annotation_set=instance).first()
        if not stats:
            return []
        return stats.statistics.get('top3_classes', [])

    def get_total_classes(self, instance):
        stats = AnnotationSetStatistics.objects.filter(annotation_set=instance).first()
        if not stats:
            return 0
        return stats.statistics.get('total_classes', 0)

    def get_total_annotation_objects(self, instance):
        return instance.annotations.aggregate(cnt=Count('annotation_objects__id'))['cnt']

    def get_is_completed(self, instance):
        annotated_images_count = instance.annotations.count()
        images_count = DatasetImage.objects.filter(dataset=instance.dataset).count()

        return annotated_images_count >= images_count > 0  # Always False if dataset is empty

    def get_is_public(self, instance):
        return instance.dataset.is_public

    def validate_task(self, data):
        # TODO: check built-in validation
        try:
            Task.objects.get(pk=data)
        except (ValueError, Task.DoesNotExist):
            raise ValidationError("bad 'task' data or such task does not exists")

    def validate(self, attrs):
        dataset = self.context['dataset']
        if not can_user_modify_dataset(self.request.user, dataset):
            raise ValidationError('Cannot modify public dataset')

    def create(self, validated_data):
        dataset = self.context['dataset']
        validated_data.update({
            'dataset': dataset,
            'user': self.request.user
        })

        return super().create(validated_data)

    class Meta:
        model = AnnotationSet
        fields = ('id', 'name', 'released_at', 'updated_at', 'task', 'annotated_images_count',
                  'total_images', 'top3_classes', 'total_classes', 'total_annotation_objects',
                  'last_annotated_date', 'is_public', 'is_completed')


class AnnotationSetLastAnnotatedSerializer(serializers.ModelSerializer):
    last_annotated = serializers.SerializerMethodField()

    def get_last_annotated(self, instance):
        # TODO: deprecated?
        return instance.dataset.id

    class Meta:
        model = AnnotationSet
        fields = ('last_annotated',)
