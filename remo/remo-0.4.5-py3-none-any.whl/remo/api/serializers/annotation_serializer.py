import logging

from rest_framework import serializers

from remo_app.remo.api.constants import AnnotationStatus, default_status
from remo_app.remo.models import (Annotation, AnnotationObjectClassRel, AnnotationClassRel)
from remo_app.remo.models import Class

logger = logging.getLogger('remo_app')


class CoordinatesSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()


class AnnotationObjectClassSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    lower = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    questionable = serializers.SerializerMethodField()

    def get_lower(self, instance):
        return instance.name.lower()

    def get_questionable(self, instance):
        qs = instance.context['rel_model_qs'].filter(annotation_class=instance)
        return qs.first().questionable

    def get_score(self, instance):
        qs = instance.context['rel_model_qs'].filter(annotation_class=instance)
        return qs.first().score


class AnnotationObjectSerializer(serializers.Serializer):
    classes = AnnotationObjectClassSerializer(many=True)
    name = serializers.CharField(max_length=255)
    coordinates = CoordinatesSerializer(many=True)
    auto_created = serializers.BooleanField(default=False)
    position_number = serializers.IntegerField(default=0)


def parse_annotation_status(data):
    status = data.get('status', default_status.name)
    try:
        if type(status) == str:
            status = AnnotationStatus.by_name(status)
        elif type(status) == int:
            status = AnnotationStatus(status)
        else:
            status = default_status
    except ValueError:
        status = default_status

    return status


class AnnotationCreateUpdateObjectSerializer(serializers.ModelSerializer):
    """
    Serializer for 'Object detection', 'Instance segmentation' tasks
    """
    annotation_info = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Annotation
        fields = ('id', 'image', 'annotation_set', 'created_at', 'updated_at', 'status', 'annotation_info')

    def get_status(self, instance):
        return str(instance.status)

    @staticmethod
    def convert_to_tuple(p):
        return (p['x'], p['y'])

    def convert_coordinates_to_tuple(self, coordinates):
        return tuple(map(self.convert_to_tuple, coordinates))

    def get_annotation_info(self, instance):
        annotation_info = []
        uniques = set()
        for annotation_object in instance.annotation_objects.order_by('name').all():
            t = self.convert_coordinates_to_tuple(annotation_object.coordinates)
            if t in uniques:
                continue
            uniques.add(t)
            info_obj = {
                'name': annotation_object.name,
                'coordinates': annotation_object.coordinates,
                'auto_created': annotation_object.auto_created,
                'position_number': annotation_object.position_number,
                'classes': [],
            }
            for annotation_object_rel in annotation_object.annotation_object_class_rel.all():
                info_obj['classes'].append({
                    'name': annotation_object_rel.annotation_class.name,
                    'lower': annotation_object_rel.annotation_class.name.lower(),
                    'questionable': annotation_object_rel.questionable
                })
            annotation_info.append(info_obj)

        return annotation_info

    def create(self, validated_data):
        skip_new_classes = self.initial_data.get('skip_new_classes', False)
        annotation_info = validated_data.pop(
            'annotation_info', self.initial_data.get('annotation_info', [])
        )
        status = parse_annotation_status(self.initial_data)

        serializer = AnnotationObjectSerializer(data=annotation_info, many=True)
        serializer.is_valid(raise_exception=True)

        annotation = Annotation.objects.filter(image=validated_data.get('image'),
                                               annotation_set=validated_data.get('annotation_set')).first()
        if not annotation:
            annotation = super().create(validated_data)

        # annotation.status = status
        annotation.save()

        self._save_annotation_objects(annotation, annotation_info, skip_new_classes)

        return annotation

    def update(self, annotation, validated_data):
        skip_new_classes = self.initial_data.get('skip_new_classes', False)

        annotation_info = validated_data.pop(
            'annotation_info', self.initial_data.get('annotation_info', [])
        )
        status = parse_annotation_status(self.initial_data)

        serializer = AnnotationObjectSerializer(data=annotation_info, many=True)
        serializer.is_valid(raise_exception=True)

        annotation = super().update(annotation, validated_data)
        # annotation.status = status
        annotation.save()
        annotation.annotation_objects.all().delete()

        # if status != AnnotationStatus.skipped and not len(annotation_info):
        #     Annotation.objects.get(id=annotation.id).delete()

        self._save_annotation_objects(annotation, annotation_info, skip_new_classes)

        return annotation

    def _save_annotation_objects(self, instance, annotation_info, skip_new_classes=False):
        classes = {}
        annotation_set = instance.annotation_set
        annotation_set_classes = {class_obj.name for class_obj in annotation_set.classes.distinct()}

        for annotation in annotation_info:
            try:
                annotation_object = instance.annotation_objects.create(
                    annotation=instance,
                    coordinates=annotation.get('coordinates', []),
                    auto_created=annotation.get('auto_created', False),
                    name=annotation.get('name', ''),
                    position_number=annotation.get('position_number', 1)
                )
            except Exception:
                continue

            for annotation_class in annotation.get('classes', []):
                class_name = annotation_class['name']
                if skip_new_classes and class_name not in annotation_set_classes:
                    continue

                try:
                    if class_name not in classes:
                        classes[class_name], _ = Class.objects.get_or_create(name=class_name)
                    annotation_class_object = classes[class_name]

                    if class_name not in annotation_set_classes:
                        annotation_set.classes.add(annotation_class_object.id)
                        annotation_set.save()
                        annotation_set_classes.add(class_name)
                except Class.DoesNotExist:
                    logger.error(f'Unknown class: {class_name}')
                    continue

                AnnotationObjectClassRel(
                    annotation_object=annotation_object,
                    annotation_class=annotation_class_object,
                    questionable=annotation_class.get('questionable', False)
                ).save()




class AnnotationCreateUpdateClassSerializer(serializers.ModelSerializer):
    """Serializer for 'Image classification task'"""
    annotation_info = serializers.SerializerMethodField()

    def get_annotation_info(self, instance):
        annotation_info = []

        qs = instance.annotation_class_rel.order_by('annotation_class__name')
        for annotation_rel in qs.all():
            obj = {
                'name': annotation_rel.annotation_class.name,
                'lower': annotation_rel.annotation_class.name.lower(),
                'questionable': annotation_rel.questionable
            }
            if annotation_rel.score is not None:
                obj['score'] = annotation_rel.score

            annotation_info.append(obj)

        return annotation_info

    def create(self, validated_data):
        skip_new_classes = self.initial_data.get('skip_new_classes', False)
        annotation_info = validated_data.pop(
            'annotation_info', self.initial_data.get('annotation_info', [])
        )
        status = parse_annotation_status(validated_data)

        serializer = AnnotationObjectClassSerializer(data=annotation_info, many=True)
        serializer.is_valid(raise_exception=True)

        annotation = super().create(validated_data)
        # annotation.status = status
        annotation.save()

        self._save_annotation_classes(annotation, annotation_info, skip_new_classes)

        return annotation

    def update(self, annotation, validated_data):
        skip_new_classes = self.initial_data.get('skip_new_classes', False)
        annotation_info = validated_data.pop(
            'annotation_info', self.initial_data.get('annotation_info', [])
        )
        status = parse_annotation_status(validated_data)

        serializer = AnnotationObjectClassSerializer(data=annotation_info, many=True)
        serializer.is_valid(raise_exception=True)

        annotation = super().update(annotation, validated_data)
        # annotation.status = status
        annotation.save()
        annotation.classes.clear()
        self._save_annotation_classes(annotation, annotation_info, skip_new_classes)

        return annotation

    def _save_annotation_classes(self, instance, annotation_info, skip_new_classes=False):
        classes = {}
        annotation_set = instance.annotation_set
        annotation_set_classes = {class_obj.name for class_obj in annotation_set.classes.distinct()}

        for annotation_class in annotation_info:
            class_name = annotation_class.get('name')
            if skip_new_classes and class_name not in annotation_set_classes:
                continue

            try:
                if class_name not in classes:
                    classes[class_name], _ = Class.objects.get_or_create(name=class_name)
                annotation_class_object = classes[class_name]

                if class_name not in annotation_set_classes:
                    annotation_set.classes.add(annotation_class_object.id)
                    annotation_set.save()
                    annotation_set_classes.add(class_name)
            except Class.DoesNotExist:
                logger.error(f'Unknown class: {class_name}')
                continue

            AnnotationClassRel(
                annotation=instance,
                annotation_class=annotation_class_object,
                questionable=annotation_class.get('questionable', False),
                score=annotation_class.get('score')
            ).save()

    class Meta:
        model = Annotation
        fields = ('id', 'image', 'annotation_set', 'created_at', 'updated_at', 'status',
                  'annotation_info')
