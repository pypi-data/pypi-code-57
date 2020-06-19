from rest_framework import mixins
from rest_framework.decorators import action
from django.db.models import Count, Q
from rest_framework import serializers
from rest_framework.response import Response

from remo_app.remo.models import Annotation, AnnotationSet, AnnotationClassRel, AnnotationObject, AnnotationTags, \
    Dataset, Tag, DatasetImage
from remo_app.remo.api.constants import TaskType, default_status, AnnotationStatus
from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.api.serializers.dataset_serializer import DatasetImageDatasetSerializer


class DatasetImageSerializer(serializers.ModelSerializer):
    original = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    view = serializers.SerializerMethodField()
    name = serializers.CharField(source='original_name')
    dataset = DatasetImageDatasetSerializer(read_only=True)
    dimensions = serializers.SerializerMethodField()
    view_dimensions = serializers.SerializerMethodField()
    image_dimensions = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    class Meta:
        model = DatasetImage
        fields = ('id', 'original', 'image', 'view', 'name', 'dataset',
                  'dimensions', 'view_dimensions', 'image_dimensions', 'status', 'annotations')

    def get_original(self, instance):
        return instance.original_url()

    def get_image(self, instance):
        return instance.image_url()

    def get_view(self, instance):
        return instance.view_url()

    def get_dimensions(self, instance):
        return instance.dimensions()

    def get_view_dimensions(self, instance):
        return instance.view_dimensions()

    def get_image_dimensions(self, instance):
        return instance.image_dimensions()

    def get_status(self, instance):
        annotation = Annotation.objects.filter(image=instance).first()
        return AnnotationStatus(getattr(annotation, 'status', default_status.value)).name

    @staticmethod
    def count_classes(classes, init_counts=None):
        counts = {}
        if init_counts:
            counts = init_counts
        for name in classes:
            counts[name] = counts.get(name, 0) + 1
        return counts

    def get_annotations(self, instance):
        annotation_sets = AnnotationSet.objects.filter(dataset=instance.dataset).all()

        result = {}
        for s in annotation_sets:
            result[s.id] = {'annotation_set': {'id': s.id, 'name': s.name, 'task': s.task.name},
                            'tags': [], 'classes': {}, 'objects': []}
            classes = s.classes.values_list('name', flat=True).all()
            result[s.id]['classes'] = {name: 0 for name in classes}
            if s.task.name == TaskType.image_classification.value:
                db_annotation = Annotation.objects.filter(image_id=instance.id, annotation_set_id=s.id)
                if db_annotation.exists():
                    db_annotation = db_annotation.first()
                    class_rels = AnnotationClassRel.objects.filter(annotation=db_annotation)
                    classes = {class_rel.annotation_class.name: class_rel.score for class_rel in class_rels.all()}
                    result[s.id]['classes'] = self.count_classes(classes, result[s.id]['classes'])

        tags = AnnotationTags.objects.filter(
            image=instance,
        ).values_list(
            'tag__name', 'annotation_set__id', 'tag__id'
        ).distinct()

        for name, annotation_set_id, id in tags:
            data = result.get(annotation_set_id, {})
            arr = data.get('tags', [])
            arr.append({'id': id, 'name': name})
            data['tags'] = arr
            result[annotation_set_id] = data

        annotation_objects = AnnotationObject.objects.filter(
            annotation__image=instance,
        ).all()

        for obj in annotation_objects:
            annotation_set_id = obj.annotation.annotation_set.id
            obj_id = obj.id
            name = obj.name
            coordinates = obj.coordinates
            classes = obj.classes.values_list('name', flat=True).all()
            data = result.get(annotation_set_id, {})
            arr = data.get('objects', [])
            arr.append({'id': obj_id, 'name': name, 'coordinates': coordinates, 'classes': classes})
            data['objects'] = arr

            class_counts = data.get('classes', {})
            for name in classes:
                class_counts[name] = class_counts.get(name, 0) + 1
            data['classes'] = class_counts
            result[annotation_set_id] = data

        return result.values()


class ShortDatasetImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(source='image_object.thumbnail.url')
    name = serializers.CharField(source='original_name')
    annotates_count = serializers.SerializerMethodField()

    class Meta:
        model = DatasetImage
        fields = ('id', 'name', 'thumbnail', 'annotates_count')

    def get_annotates_count(self, instance):
        """
        Return count of annotation objects (object detection),
        annotated classes (image classification)
        """
        qs = Annotation.objects.filter(image=instance).all()
        if not qs.count():
            return 0
        return qs.aggregate(Count('classes'))['classes__count'] + \
               qs.aggregate(Count('annotation_objects'))['annotation_objects__count']


class DatasetImages(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    BaseNestedModelViewSet):
    parent_lookup = 'datasets'
    serializer_class = DatasetImageSerializer

    serializer_action_classes = {
        'retrieve': DatasetImageSerializer,
        'list': ShortDatasetImageSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_parent_queryset(self):
        return Dataset.objects.filter(
            Q(user=self.request.user) | Q(is_public=True),
            is_archived=False
        )

    def get_queryset(self):
        return DatasetImage.objects.filter(
            dataset=self.parent_pk,
        )

    @action(['get'], detail=True, url_path='annotations')
    def annotations(self, request, *args, **kwargs):
        image = DatasetImage.objects.filter(id=kwargs['pk']).first()
        return Response(DatasetImageSerializer(image).data)
