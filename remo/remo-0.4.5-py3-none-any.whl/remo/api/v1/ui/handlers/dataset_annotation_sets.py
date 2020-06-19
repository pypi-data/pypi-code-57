from rest_framework import serializers
from rest_framework import mixins
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import AnnotationSet, AnnotationSetStatistics, Task, Dataset, DatasetImage
from remo_app.remo.stores.image_store import ImageStore


class ShortTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'type')


class DatasetAnnotationSetSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    updated_at = serializers.DateTimeField(read_only=True)
    task = ShortTaskSerializer()
    is_public = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    total_images = serializers.IntegerField(source='dataset.quantity', read_only=True)

    statistics = serializers.SerializerMethodField()

    class Meta:
        model = AnnotationSet
        fields = ('id', 'name', 'released_at', 'updated_at', 'task', 'total_images',
                  'last_annotated_date', 'is_public', 'is_completed', 'statistics',)

    def get_statistics(self, instance):
        stats = AnnotationSetStatistics.objects.filter(annotation_set=instance).first()
        if not stats:
            return {
                'annotated_images_count': 0,
                'skipped_count': 0,
                'top3_classes': [],
                'all_classes': [],
                'total_classes': 0,
                'total_annotation_objects': 0,
                'images_without_annotations': 0
            }

        top3_classes = []
        if stats.top3_classes:
            top3 = stats.top3_classes
            top3_classes = [{'name': pair[1], 'count': pair[0]} for pair in top3]

        all_classes = []
        for class_name, class_stat in stats.classes.items():
            n_objs = class_stat.get('n_objs', class_stat.get('n_imgs', 0))
            all_classes.append({
                'name': class_name,
                'count': n_objs,
            })

        images_without_annotations = ImageStore.calc_images_without_annotations(instance.id)
        return {
            'annotated_images_count': stats.total_annotated_images,
            'skipped_count': stats.skipped_images,
            'top3_classes': top3_classes,
            'all_classes': all_classes,
            'total_classes': stats.total_classes,
            'total_annotation_objects': stats.total_annotation_objects,
            'images_without_annotations': images_without_annotations
        }

    def get_is_completed(self, instance):
        annotated_images_count = instance.annotations.count()
        images_count = DatasetImage.objects.filter(dataset=instance.dataset).count()

        return annotated_images_count >= images_count > 0  # Always False if dataset is empty

    def get_is_public(self, instance):
        return instance.dataset.is_public


class DatasetAnnotationSets(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            BaseNestedModelViewSet):
    parent_lookup = 'datasets'
    filter_backends = (DjangoFilterBackend,)
    serializer_class = DatasetAnnotationSetSerializer

    def get_parent_queryset(self):
        return Dataset.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        ).filter(is_archived=False)

    def get_queryset(self):
        # TODO: restrict to team when it will be implemented, #272
        dataset = self.get_parent_object_or_404()
        return AnnotationSet.objects.filter(dataset=dataset)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['dataset'] = self.get_parent_object_or_404()
        return ctx
