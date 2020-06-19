import io
import zipfile
import json
from typing import List

from django.http import HttpResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q

from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from remo_app.remo.use_cases.annotation.class_encoding.factory import class_encoding_factory
from remo_app.remo.use_cases.annotation.export_tags import export_tags_for_annotation_set
from remo_app.remo.use_cases.annotation.formats import get_exporter
from remo_app.remo.models import AnnotationSet
from remo_app.remo.api.serializers import (
    CommonClassSerializer,
    TaskSerializer,
    UserDatasetSerializer,
    CommonClassNestedSerializer
)
from remo_app.remo.api.shortcuts import can_user_modify_annotation_set
from remo_app.remo.models import Task, Dataset, Class
from remo_app.remo.use_cases.annotation_tasks import parse_annotation_task
from remo_app.remo.use_cases.classes import capitalize_class_name
from remo_app.remo.use_cases.duplicates import copy_annotation_set
from remo_app.remo.api.constants import TaskType, AnnotationSetType
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.use_cases.annotation.class_encoding import class_encoding


class AnnotationSetSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=False)
    classes = CommonClassSerializer(many=True, required=False)
    dataset = UserDatasetSerializer(many=False, required=False)

    is_last_modified = serializers.SerializerMethodField()
    is_public = serializers.SerializerMethodField()

    def get_is_last_modified(self, obj):
        # TODO: probably obsolete
        return False

    def get_is_public(self, instance):
        return instance.dataset.is_public

    class Meta:
        model = AnnotationSet
        fields = ('id', 'name', 'released_at', 'updated_at', 'task', 'dataset',
                  'last_annotated_date', 'classes', 'is_last_modified', 'type',
                  'is_public')


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


class AnnotationSets(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    ordering = 'pk'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'duplicate'):
            return AnnotationSetSerializer
        return AnnotationSetModifySerializer

    def get_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def update(self, request, *args, **kwargs):
        id = kwargs['pk']
        annotation_set = AnnotationSet.objects.filter(id=id).first()
        if annotation_set is None:
            return Response({'error': f'Annotation set with id: {id}, was not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        if not can_user_modify_annotation_set(request.user, annotation_set):
            return Response({'error': 'Public annotation set "{}" is read-only'.format(id)},
                            status=status.HTTP_403_FORBIDDEN)

        data = json.loads(request.body)
        name = data.get('name')
        if name is None:
            return Response({'error': f'Name is required field, was missing.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(name, str):
            return Response({'error': f'Name should be a string value.'},
                            status=status.HTTP_400_BAD_REQUEST)
        name = name.strip()
        if name != annotation_set.name:
            if AnnotationSet.objects.filter(dataset=annotation_set.dataset, name=name).exists():
                return Response({'error': f"Annotation set with giving name '{name}', exists in current dataset."},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                annotation_set.name = name
                annotation_set.save()
            except Exception as err:
                return Response({'error': 'Failed to rename annotation set "{}": {}'.format(id, err)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'id': annotation_set.id,
            'name': name,
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)

        name, annotation_task, dataset, classes, resp = self._validate_create_data(data)
        if resp:
            return resp

        task = Task.objects.get(type=annotation_task.name)
        annotation_set = AnnotationSet.objects.create(
            name=name,
            type=AnnotationSetType.image.value,
            task=task,
            user=dataset.user,
            dataset=dataset
        )

        # add classes to annotation-set
        result_classes = {}
        for class_name in classes:
            class_name = capitalize_class_name(class_name)
            obj, _ = Class.objects.get_or_create(name=class_name)
            annotation_set.classes.add(obj.id)
            result_classes[obj.id] = class_name

        annotation_set.save()
        update_annotation_set_statistics(annotation_set)

        result_classes = [{"id": id, "name": name} for id, name in result_classes.items()]

        return Response({
            'id': annotation_set.id,
            'name': name,
            'task': task.name,
            'dataset_id': dataset.id,
            'classes': result_classes
        }, status=status.HTTP_201_CREATED)

    def _validate_create_data(self, data):
        annotation_task, resp = self._validate_annotation_task(data)
        if resp:
            return None, None, None, None, resp

        dataset, resp = self._validate_dataset_id(data)
        if resp:
            return None, None, None, None, resp

        name, resp = self._validate_name(data, dataset.id)
        if resp:
            return None, None, None, None, resp

        classes, resp = self._validate_classes(data)
        if resp:
            return None, None, None, None, resp

        return name, annotation_task, dataset, classes, None

    def _validate_classes(self, data):
        classes = data.get('classes', [])
        if not isinstance(classes, list):
            return None, Response({'error': f'Classes should be a list of strings'},
                                  status=status.HTTP_400_BAD_REQUEST)

        if len(classes) and any(not isinstance(name, str) for name in classes):
            return None, Response({'error': f'Classes should be a list of strings'},
                                  status=status.HTTP_400_BAD_REQUEST)

        classes = list(filter(lambda v: len(v),
                              map(lambda v: v.strip(), set(classes))
                              )
                       )
        return classes, None

    def _validate_name(self, data, dataset_id):
        name = data.get('name')
        if name is None:
            return None, Response({'error': f'Name is required field, was missing.'},
                                  status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(name, str):
            return None, Response({'error': f'Name should be a string value.'},
                                  status=status.HTTP_400_BAD_REQUEST)
        name = name.strip()
        if AnnotationSet.objects.filter(dataset_id=dataset_id, name=name).exists():
            return None, Response({'error': f"Annotation set with giving name '{name}', exists in current dataset."},
                                  status=status.HTTP_400_BAD_REQUEST)
        return name, None

    def _validate_annotation_task(self, data):
        task = data.get('annotation_task')
        annotation_task = parse_annotation_task(task)
        if annotation_task is None:
            return None, Response({'error': f"Annotation task '{task}' not recognized. "
                                            f'Try one of this: {", ".join(map(lambda t: t[1], TaskType.choices()))}.'},
                                  status=status.HTTP_400_BAD_REQUEST)
        return annotation_task, None

    def _validate_dataset_id(self, data):
        value = data.get('dataset_id')
        dataset_id = self._parse_int_param(value)
        if dataset_id is None:
            return None, Response({'error': f'Dataset id: {value}, not a valid id.'},
                                  status=status.HTTP_400_BAD_REQUEST)

        dataset = Dataset.objects.filter(id=dataset_id).first()
        if dataset is None:
            return None, Response({'error': f'Dataset with id: {dataset_id}, was not found.'},
                                  status=status.HTTP_404_NOT_FOUND)

        if self.request.user != dataset.user:
            # TODO: check later in dataset.users_shared
            return None, Response({
                'error': 'Only dataset owner can create new annotation set.',
            }, status=status.HTTP_403_FORBIDDEN)

        return dataset, None

    def _parse_int_param(self, value):
        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            return None

    def _validate_annotation_set(self, id: int):
        annotation_set = AnnotationSet.objects.filter(id=id).first()
        if annotation_set is None:
            return None, Response({'error': f'Annotation set with id: {id}, was not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        return annotation_set, None

    @staticmethod
    def _boolean_value(value: str) -> bool:
        return value == 'true'

    @staticmethod
    def _validate_query_parameter(value: str, name: str, allowed_values: List[str]):
        if value not in allowed_values:
            if len(allowed_values) >= 2:
                allowed_values = ', '.join(allowed_values[:-1]) + f' or {allowed_values[-1]}'
            return Response(
                {'error': f'Exporter parameter {name} can be: {allowed_values}'},
                status=status.HTTP_400_BAD_REQUEST)

    def _validate_boolean_parameter(self, value: str, name: str):
        return self._boolean_value(value), self._validate_query_parameter(value, name, ['true', 'false'])

    @action(['get'], detail=True, url_path='export')
    def export(self, request, *args, **kwargs):
        annotation_format = request.query_params.get('annotation_format', 'json')
        resp = self._validate_query_parameter(annotation_format, 'annotation_format', ['coco', 'json', 'csv'])
        if resp:
            return resp

        full_path = request.query_params.get('full_path', 'false')
        full_path, resp = self._validate_boolean_parameter(full_path, 'full_path')
        if resp:
            return resp

        # TODO: add export classes
        export_classes = request.query_params.get('export_classes', 'false')
        export_classes, resp = self._validate_boolean_parameter(export_classes, 'export_classes')
        if resp:
            return resp

        export_coordinates = request.query_params.get('export_coordinates', 'pixel')
        resp = self._validate_query_parameter(export_coordinates, 'export_coordinates', ['pixel', 'percent'])
        if resp:
            return resp

        export_without_annotations = request.query_params.get('export_without_annotations', 'false')
        export_without_annotations, resp = self._validate_boolean_parameter(export_without_annotations, 'export_without_annotations')
        if resp:
            return resp

        export_tags = request.query_params.get('export_tags', 'false')
        export_tags, resp = self._validate_boolean_parameter(export_tags, 'export_tags')
        if resp:
            return resp

        annotation_set, resp = self._validate_annotation_set(kwargs['pk'])
        if resp:
            return resp

        task = parse_annotation_task(annotation_set.task.name)
        exporter_class = get_exporter(task, annotation_format)
        if not exporter_class:
            return Response({'error': f'Exporter for {task} task in format {annotation_format} not implemented'},
                            status=404)

        encoding_type = request.query_params.get('class_encoding', None)
        if encoding_type and encoding_type not in class_encoding.types:
            return Response({'error': f'Exporter parameter class_encoding: {class_encoding}, not valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

        exporter = exporter_class()
        if encoding_type:
            encoding = class_encoding_factory.get(encoding_type)
            exporter.class_encoding = encoding

        ext = {
            "coco": "json",
        }.get(annotation_format, annotation_format)
        filename = f'{annotation_set.name}.{ext}'

        output = exporter.export_annotations(annotation_set, export_coordinates=export_coordinates, full_path=full_path,
                                             export_classes=export_classes, export_without_annotations=export_without_annotations)

        if not export_tags:
            content_type = {
                "coco": "application/json",
                "json": "application/json",
                "csv": "text/csv",
            }.get(annotation_format, 'text/plain')
            headers = {
                "Content-Disposition": f'filename="{filename}"',
                "Content-Type": content_type
            }
            response = HttpResponse(content=bytes(output, 'UTF-8'), content_type=content_type)
            response["Content-Disposition"] = headers["Content-Disposition"]
            return response

        tags_csv = export_tags_for_annotation_set(annotation_set)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip:
            zip.writestr('tags.csv', tags_csv)
            zip.writestr(filename, output)

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response["Content-Disposition"] = f'attachment; filename="annotations.zip"'
        return response

    @action(['post'], detail=True, url_path='duplicate')
    def duplicate(self, request, *args, **kwargs):
        annotation_set = AnnotationSet.objects.get(id=kwargs['pk'])
        annotation_set = copy_annotation_set(annotation_set)
        serializer = self.get_serializer_class()(annotation_set, context={'request': request})

        return Response(serializer.data)
