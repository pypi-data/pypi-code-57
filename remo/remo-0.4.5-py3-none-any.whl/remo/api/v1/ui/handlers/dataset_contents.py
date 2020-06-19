from django.conf import settings
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from queryset_sequence import QuerySetSequence
from django.db.models import Q
from rest_framework import serializers
from rest_framework.utils.urls import replace_query_param

from remo_app.remo.api.v1.ui.handlers.search import Search
from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import (
    Dataset,
    Annotation,
    NewAnnotation,
    DatasetImage,
    ImageFolder,
    ImageFolderStatistics,
    AnnotationSet,
)


class BriefUserDatasetFolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    dataset_id = serializers.IntegerField(source='dataset.id', read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    preview = serializers.SerializerMethodField()
    total_images = serializers.SerializerMethodField()
    top3_classes = serializers.SerializerMethodField()
    total_classes = serializers.SerializerMethodField()

    class Meta:
        model = ImageFolder
        fields = (
            'id',
            'name',
            'dataset_id',
            'updated_at',
            'created_at',
            'preview',
            'total_images',
            'top3_classes',
            'total_classes',
        )

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


class DatasetImageSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    name = serializers.CharField(source='original_name')
    dimensions = serializers.SerializerMethodField()
    size_in_bytes = serializers.IntegerField(source='image_object.size')
    annotations = serializers.SerializerMethodField()

    class Meta:
        model = DatasetImage
        fields = ('id', 'view', 'preview', 'name', 'annotations', 'dimensions', 'size_in_bytes', 'created_at')

    def get_view(self, instance):
        return instance.view_url()

    def get_preview(self, instance):
        return instance.preview_url()

    def get_dimensions(self, instance):
        return [instance.image_object.width, instance.image_object.height]

    def get_annotations(self, instance):
        all_annotations = []
        indexes = {}
        annotation_sets = AnnotationSet.objects.filter(dataset=instance.dataset)
        for annotation_set in annotation_sets:
            indexes[annotation_set.id] = len(all_annotations)
            all_annotations.append(
                {
                    'annotation_set_id': annotation_set.id,
                    'coordinates': [],
                    'classes': [],
                    'object_classes': [],
                }
            )

        annotation_sets = (
            Annotation.objects.filter(image=instance,).values_list('annotation_set__pk', flat=True).distinct()
        )

        for annotation_set_id in annotation_sets:
            annotations = self.get_annotation_set_annotations(instance, annotation_set_id)
            all_annotations[indexes[annotation_set_id]].update(annotations)

        return all_annotations

    def get_annotation_set_annotations(self, instance, annotation_set_id):
        coordinates, object_classes = self.get_coordinates(instance, annotation_set_id)
        annotations = {
            'coordinates': coordinates,
            'object_classes': object_classes,
            'classes': [],
        }

        if not coordinates:
            annotations['classes'] = self.get_classes(instance, annotation_set_id)

        return annotations

    def get_classes(self, instance, annotation_set_id):
        annotation = NewAnnotation.objects.filter(
            image=instance, annotation_set__pk=annotation_set_id
        ).first()

        classes = []
        if annotation and annotation.classes:
            classes = annotation.classes

        return classes

    def get_coordinates(self, instance, annotation_set_id):
        annotation = NewAnnotation.objects.filter(
            image=instance, annotation_set__pk=annotation_set_id
        ).first()

        coordinates = []
        object_classes = []
        if annotation and annotation.data and annotation.data.get('objects'):
            for obj in annotation.data.get('objects'):
                coordinates.append(obj.get('coordinates', []))
                object_classes.append(obj.get('classes', []))

        if len(coordinates) == 1 and len(coordinates[0]) == 0:
            coordinates = []

        return coordinates, object_classes


class DatasetContentsSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        return self._get_instance_type(instance)

    def get_image(self, instance):
        if self._get_instance_type(instance) != 'image':
            return None

        return DatasetImageSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        if self._get_instance_type(instance) != 'folder':
            return None

        return BriefUserDatasetFolderSerializer(instance, context=self.context).data

    def _get_instance_type(self, instance):
        types = {ImageFolder: 'folder', DatasetImage: 'image'}
        return types.get(type(instance))


class SearchDatasetContentsSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        return "image"

    def get_image(self, instance):
        return SearchDatasetImageSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        return None


class SearchDatasetImageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='image_id')
    view = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    name = serializers.CharField(source='image.original_name')
    dimensions = serializers.SerializerMethodField()
    size_in_bytes = serializers.IntegerField(source='image.image_object.size')
    annotations = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='image.created_at')

    class Meta:
        model = NewAnnotation
        fields = ('id', 'view', 'preview', 'name', 'annotations', 'dimensions', 'size_in_bytes', 'created_at')

    def get_view(self, instance):
        return instance.image.view_url()

    def get_preview(self, instance):
        return instance.image.preview_url()

    def get_dimensions(self, instance):
        return [instance.image.image_object.width, instance.image.image_object.height]

    def get_annotations(self, instance):
        coordinates = []
        object_classes = []
        classes = set()
        for obj in instance.data['objects']:
            coordinates.append(obj.get('coordinates', []))
            obj_classes = obj.get('classes')
            object_classes.append(obj_classes)

            if obj_classes:
                classes = classes.union(obj_classes)

        return [
            {
                'annotation_set_id': instance.annotation_set_id,
                'coordinates': coordinates,
                'object_classes': object_classes,
                'classes': list(classes),
            }
        ]


class DatasetContents(mixins.ListModelMixin, mixins.RetrieveModelMixin, BaseNestedModelViewSet):
    parent_lookup = 'datasets'
    serializer_class = DatasetContentsSerializer
    direct_name = 'direction'

    def get_parent_queryset(self):
        return Dataset.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def get_contents(self, folder_object=None):
        """
        Return contents of dataset folder
        :param folder_object: folder to list contents of, Default: root
        :return: Response object with paginated results
        """
        folders = ImageFolder.objects.filter(dataset=self.parent_pk)
        images = DatasetImage.objects.filter(dataset=self.parent_pk)

        if folder_object:
            images = images.filter(folder=folder_object)
        else:
            images = images.filter(folder__isnull=True)
        folders = folders.filter(parent=folder_object)

        queryset = QuerySetSequence(folders, images)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        image_id = self._parse_int_param(request.query_params.get('image_id'), min_value=1)
        dataset_id = self.parent_pk

        default_limit = settings.REST_FRAMEWORK['PAGE_SIZE']
        limit = self._parse_int_param(request.query_params.get('limit', default_limit), default_limit, 1)
        direction = request.query_params.get(self.direct_name)

        classes = request.query_params.get('classes')
        classes_not = request.query_params.get('classes_not')
        tags = request.query_params.get('tags')
        tags_not = request.query_params.get('tags_not')
        tasks = request.query_params.get('tasks')
        tasks_not = request.query_params.get('tasks_not')

        if classes or classes_not or tags or tags_not or tasks or tasks_not:
            page = Search().execute(
                dataset_id, image_id, direction, limit, classes, classes_not, tags, tags_not, tasks, tasks_not
            )
            kw = {'context': {'request': self.request, 'view': self}}
            serializer = SearchDatasetContentsSerializer(page, many=True, **kw)
            data = serializer.data
            resp = self._paginate_resp(data, limit, image_id, direction)
            return Response(resp)

        return self.get_contents(folder_object=None)

    def _paginate_resp(self, data, limit, image_id, direction):
        next_url = None
        prev_url = None
        left, right = 0, len(data)
        if len(data) > limit:
            image_index = self._get_image_index(data, image_id)
            left, right = self.filter_range(image_index, limit, len(data))

        if left > 0 and direction != Search.next_direct:
            prev_url = self._create_url(data[left]['image_id'], Search.prev_direct)
        if right < len(data) and direction != Search.prev_direct:
            next_url = self._create_url(data[right - 1]['image_id'], Search.next_direct)

        results = data[left:right]

        return {'count': len(results), 'next': next_url, 'previous': prev_url, 'results': results}

    def _create_url(self, img_id, direction):
        current_url = self.request.get_full_path()
        url = replace_query_param(current_url, 'image_id', img_id)
        return replace_query_param(url, 'direction', direction)

    @staticmethod
    def _get_image_index(data, image_id):
        if not image_id:
            return

        for index, img in enumerate(data):
            if img['image_id'] >= image_id:
                return index

    @staticmethod
    def filter_range(img_idx: int, limit: int, size: int):
        if img_idx is None:
            return 0, limit

        half = int(limit / 2)
        left = img_idx - half
        right = img_idx + limit - half

        if left < 0:
            rest = -left
            left = 0
            right += rest
        elif right > size:
            rest = right - size
            right = size
            left -= rest

        return left, right

    @staticmethod
    def _parse_int_param(value, default=None, min_value: int = None):
        if value:
            try:
                value = int(value)
                if min_value:
                    value = max(value, min_value)
            except ValueError:
                value = default
        return value

    def retrieve(self, request, *args, **kwargs):
        # TODO: make walk contents/folder1/folder2/..., #333
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        fltr = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(ImageFolder, **fltr)
        return self.get_contents(obj)
