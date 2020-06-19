from django.db.models import Count, Q
from rest_framework import serializers

from remo_app.remo.models import Annotation, AnnotationObject, AnnotationSet, AnnotationClassRel, AnnotationTags, \
    DatasetImage
from remo_app.remo.api.constants import TaskType, default_status, AnnotationStatus
from remo_app.remo.api.serializers.dataset_serializer import DatasetImageDatasetSerializer


class DatasetImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    view = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    name = serializers.CharField(source='original_name')
    dataset = DatasetImageDatasetSerializer(read_only=True)
    dataset_id = serializers.IntegerField(source='dataset.id')
    dimensions = serializers.SerializerMethodField()
    annotates_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    tags_count = serializers.SerializerMethodField()
    annotations_count = serializers.SerializerMethodField()
    classes = serializers.SerializerMethodField()
    # @deprecated
    coordinates = serializers.SerializerMethodField()
    size_in_bytes = serializers.IntegerField(source='image_object.image.size')

    def get_image(self, instance):
        return instance.image_url()

    def get_thumbnail(self, instance):
        return instance.thumbnail_url()

    def get_view(self, instance):
        return instance.view_url()

    def get_preview(self, instance):
        return instance.preview_url()

    def get_dimensions(self, instance):
        return instance.dimensions()

    def get_annotates_count(self, instance):
        """
        Return count of annotation objects (object detection),
        annotated classes (image classification)
        """
        user = self.context.get('request').user
        qs = Annotation.objects.filter(image=instance, annotation_set__user=user).all()
        if not qs.count():
            return 0
        return qs.aggregate(Count('classes'))['classes__count'] + \
               qs.aggregate(Count('annotation_objects'))['annotation_objects__count']

    def get_status(self, instance):
        user = self.context.get('request').user
        annotation = Annotation.objects.filter(image=instance, annotation_set__user=user).first()
        return str(getattr(annotation, 'status', default_status))

    def get_tags_count(self, instance):
        user = self.context.get('request').user
        return AnnotationTags.objects.filter(image=instance, annotation_set__user=user).count()

    def get_annotations_count(self, instance):
        user = self.context.get('request').user
        return Annotation.objects.filter(image=instance, annotation_set__user=user).count()

    def get_classes(self, instance):
        user = self.context.get('request').user
        classes = Annotation.objects.filter(
            Q(annotation_set__user=user) | Q(annotation_set__dataset__is_public=True), image=instance
        ).exclude(
            classes=None
        ).values_list(
            'classes__name', flat=True
        ).order_by('classes__name').distinct('classes__name').all()

        return classes

    def get_coordinates(self, instance):
        user = self.context.get('request').user
        coordinates = Annotation.objects.filter(
            Q(annotation_set__user=user) | Q(annotation_set__dataset__is_public=True), image=instance
        ).exclude(
            annotation_objects=None
        ).values_list(
            'annotation_objects__coordinates', flat=True
        ).order_by('annotation_objects__id').all()

        return coordinates

    class Meta:
        model = DatasetImage
        fields = ('id', 'image', 'thumbnail', 'view', 'preview', 'name', 'dataset',
                  'dataset_id', 'dimensions', 'annotates_count', 'status', 'tags_count',
                  'annotations_count', 'classes', 'coordinates', 'number_in_dataset', 'size_in_bytes', 'created_at'
                  )


class AnnotationSetImageSerializer(DatasetImageSerializer):
    annotates_count = serializers.SerializerMethodField()
    classes = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    original = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, instance):
        annotation_set = self.context['annotation_set']
        annotation = Annotation.objects.filter(image=instance, annotation_set=annotation_set).first()
        return AnnotationStatus(getattr(annotation, 'status', default_status.value)).name

    def get_original(self, instance):
        return instance.original_url()

    def get_image(self, instance):
        return instance.image_url()

    def get_annotates_count(self, instance):
        """
        Return count of annotation objects (object detection),
        annotated classes (image classification)
        """
        annotation_set = self.context['annotation_set']
        qs = Annotation.objects.filter(image=instance, annotation_set=annotation_set).all()
        if not qs.count():
            return 0

        annotation = qs.first()
        if annotation.annotation_set.task.type == TaskType.image_classification.name:
            return annotation.classes.count()
        else:
            return annotation.annotation_objects.count()

    def get_classes(self, instance):
        annotation_set = self.context['annotation_set']
        classes = Annotation.objects.filter(
            image=instance, annotation_set=annotation_set
        ).exclude(
            classes=None
        ).values_list(
            'classes__name', flat=True
        ).order_by('classes__name').distinct('classes__name').all()
        return classes

    def get_coordinates(self, instance):
        annotation_set = self.context['annotation_set']
        coordinates = Annotation.objects.filter(
            image=instance, annotation_set=annotation_set
        ).exclude(
            annotation_objects=None
        ).values_list(
            'annotation_objects__coordinates', flat=True
        ).order_by('annotation_objects__id').all()

        return coordinates

    class Meta:
        model = DatasetImage
        fields = ('id', 'image', 'original', 'thumbnail', 'name', 'dataset',
                  'dataset_id', 'dimensions', 'annotates_count', 'status', 'tags_count',
                  'annotations_count', 'classes', 'coordinates', 'number_in_dataset')


class AnnotationSetDatasetImageSerializer(AnnotationSetImageSerializer):
    preview_dimensions = serializers.SerializerMethodField()

    def get_preview_dimensions(self, instance):
        img_obj = instance.image_object
        if img_obj.image and img_obj.original:
            return img_obj.image_dimensions()

    class Meta:
        model = DatasetImage
        fields = ('id', 'image', 'original', 'thumbnail', 'name',
                  'dimensions', 'preview_dimensions', 'annotates_count', 'status')


# TODO: check it later for image optimizatino
class DatasetUserImageSerializer(DatasetImageSerializer):
    class Meta:
        model = DatasetImage
        fields = ('id', 'image', 'name',)


class DatasetImageAnnotationsSerializer(DatasetImageSerializer):
    annotations = serializers.SerializerMethodField()

    @staticmethod
    def count_classes(classes):
        counts = {}
        for name in classes:
            counts[name] = counts.get(name, 0) + 1
        return counts

    def get_annotations(self, instance):
        user = self.context.get('request').user

        annotation_sets_ids = Annotation.objects.filter(
            image=instance, annotation_set__user=user
        ).values_list(
            'annotation_set__id', flat=True
        ).distinct()

        annotation_sets = AnnotationSet.objects.filter(pk__in=annotation_sets_ids).all()

        result = {}
        for s in annotation_sets:
            result[s.id] = {'annotation_set': {'id': s.id, 'name': s.name, 'task': s.task.name},
                            'tags': [], 'classes': {}, 'objects': []}
            if s.task.name == TaskType.image_classification.value:
                db_annotation = Annotation.objects.filter(image_id=instance.id, annotation_set_id=s.id)
                if db_annotation.exists():
                    db_annotation = db_annotation.first()
                    class_rels = AnnotationClassRel.objects.filter(annotation=db_annotation)
                    classes = {class_rel.annotation_class.name: class_rel.score for class_rel in class_rels.all()}
                    result[s.id]['classes'] = self.count_classes(classes)

        tags = AnnotationTags.objects.filter(
            image=instance, annotation_set__user=user
        ).values_list(
            'tag__name', 'annotation_set__id'
        ).all()

        for t in tags:
            name, id = t
            data = result.get(id, {})
            arr = data.get('tags', [])
            arr.append(name)
            data['tags'] = arr
            result[id] = data

        annotation_objects = AnnotationObject.objects.filter(
            annotation__image=instance, annotation__annotation_set__user=user
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
                count = class_counts.get(name, 0)
                count += 1
                class_counts[name] = count
            data['classes'] = class_counts
            result[annotation_set_id] = data

        return result.values()

    class Meta:
        model = DatasetImage
        fields = ('id', 'image', 'thumbnail', 'view', 'preview', 'name', 'dataset',
                  'dataset_id', 'dimensions', 'annotates_count', 'status', 'tags_count',
                  'annotations_count', 'classes', 'coordinates', 'number_in_dataset', 'annotations', 'size_in_bytes',
                  'created_at')
