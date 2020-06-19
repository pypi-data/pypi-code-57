from django.conf import settings
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.utils.urls import replace_query_param

from remo_app.remo.api.v1.ui.handlers.filters import QueryBuilder, transform_filter_to_condition
from remo_app.remo.models.annotation import NewAnnotation
from remo_app.remo.use_cases.annotation_tasks import parse_annotation_task
from remo_app.remo.use_cases.classes import capitalize_class_name


class SearchImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='image.original_name')
    preview = serializers.SerializerMethodField()
    dimensions = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    class Meta:
        model = NewAnnotation
        fields = ('image_id', 'dataset_id', 'name', 'preview', 'annotations', 'dimensions')

    def get_preview(self, instance):
        return instance.image.image_object.preview.url if instance.image.image_object.preview else None

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

        return {
            'coordinates': coordinates,
            'object_classes': object_classes,
            'classes': list(classes),
        }


class SearchView(viewsets.GenericViewSet):
    queryset = NewAnnotation.objects.all()
    serializer_class = SearchImageSerializer
    ordering = 'id'

    # prev_direct = 'prev'
    # next_direct = 'next'
    direct_name = 'direction'
    # direct_operator = {
    #     prev_direct: '<',
    #     next_direct: '>',
    # }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(dataset__is_public=True) | Q(dataset__user=self.request.user))
    # def backup_list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     classes = request.query_params.get('classes')
    #     if classes:
    #         classes = classes.split(',')
    #         queryset = queryset.filter(classes__contains=classes)
    #
    #     tags = request.query_params.get('tags')
    #     if tags:
    #         tags = tags.split(',')
    #         queryset = queryset.filter(tags__contains=tags)
    #
    #     tasks = request.query_params.get('tasks')
    #     if tasks:
    #         tasks = tasks.split(',')
    #         # doesn't allowed to use multiple tasks in one query
    #         task = parse_annotation_task(tasks[0])
    #         if task:
    #             queryset = queryset.filter(task=task.name)
    #
    #     classes_not = request.query_params.get('classes_not')
    #     if classes_not:
    #         classes_not = classes_not.split(',')
    #         queryset = queryset.exclude(classes__contains=classes_not)
    #
    #     tags_not = request.query_params.get('tags_not')
    #     if tags_not:
    #         tags_not = tags_not.split(',')
    #         queryset = queryset.exclude(tags__contains=tags_not)
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        image_id = self._parse_int_param(request.query_params.get('image_id'), min_value=1)
        dataset_id = self._parse_int_param(request.query_params.get('dataset_id'), min_value=1)
        default_limit = settings.REST_FRAMEWORK['PAGE_SIZE']
        limit = self._parse_int_param(request.query_params.get('limit', default_limit), default_limit, 1)
        direction = request.query_params.get(self.direct_name)

        classes = request.query_params.get('classes')
        classes_not = request.query_params.get('classes_not')
        tags = request.query_params.get('tags')
        tags_not = request.query_params.get('tags_not')
        tasks = request.query_params.get('tasks')
        tasks_not = request.query_params.get('tasks_not')

        page = Search().execute(dataset_id, image_id, direction, limit, classes, classes_not, tags, tags_not, tasks, tasks_not)

        # classes = request.query_params.get('classes')
        # if classes:
        #     classes = classes.split(',')
        #     classes = list(map(capitalize_class_name, classes))
        #
        # classes_not = request.query_params.get('classes_not')
        # if classes_not:
        #     classes_not = classes_not.split(',')
        #     classes_not = list(map(capitalize_class_name, classes_not))
        #
        # tags = request.query_params.get('tags')
        # if tags:
        #     tags = tags.split(',')
        #
        # tags_not = request.query_params.get('tags_not')
        # if tags_not:
        #     tags_not = tags_not.split(',')
        #
        # tasks = request.query_params.get('tasks')
        # if tasks:
        #     tasks = tasks.split(',')
        #     # allowed only one task
        #     task = parse_annotation_task(tasks[0])
        #     if task:
        #         tasks = [task.name]
        #     else:
        #         tasks = []
        #
        # tasks_not = request.query_params.get('tasks_not')
        # if tasks_not:
        #     tasks_not = tasks_not.split(',')
        #     # allowed only one task
        #     task = parse_annotation_task(tasks_not[0])
        #     if task:
        #         tasks_not = [task.name]
        #     else:
        #         tasks_not = []
        #
        # filters = []
        # if classes:
        #     for name in classes:
        #         filters.append({
        #             'name': 'class',
        #             'condition': 'is',
        #             'pattern': name,
        #         })
        #
        # if classes_not:
        #     for name in classes_not:
        #         filters.append({
        #             'name': 'class',
        #             'condition': 'is_not',
        #             'pattern': name,
        #         })
        #
        # if tags:
        #     for name in tags:
        #         filters.append({
        #             'name': 'tag',
        #             'condition': 'is',
        #             'pattern': name,
        #         })
        #
        # if tags_not:
        #     for name in tags_not:
        #         filters.append({
        #             'name': 'tag',
        #             'condition': 'is_not',
        #             'pattern': name,
        #         })
        # if tasks:
        #     for name in tasks:
        #         filters.append({
        #             'name': 'task',
        #             'condition': 'is',
        #             'pattern': name,
        #         })
        #
        # if tasks_not:
        #     for name in tasks_not:
        #         filters.append({
        #             'name': 'task',
        #             'condition': 'is_not',
        #             'pattern': name,
        #         })
        #
        # qb = QueryBuilder("SELECT id FROM new_annotations")
        #
        # if dataset_id:
        #     qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))
        #
        # if image_id:
        #     comparison = self.direct_operator.get(direction)
        #     qb.condition(QueryBuilder.Condition("image_id", comparison, image_id))
        #
        # for filter in filters:
        #     qb.condition(transform_filter_to_condition(filter))
        #
        # qb.order_by("image_id")
        # qb.limit(limit + 1)

        serializer = self.get_serializer(page, many=True)
        data = serializer.data
        # data = self._query_data(qb.query())
        resp = self._paginate_resp(data, limit, image_id, direction)
        return Response(resp)

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

    def _query_data(self, query):
        page = NewAnnotation.objects.raw(query)
        serializer = self.get_serializer(page, many=True)
        return serializer.data

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

        return {
            'count': len(results),
            'next': next_url,
            'previous': prev_url,
            'results': results
        }

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



class Search:
    prev_direct = 'prev'
    next_direct = 'next'
    # direct_name = 'direction'
    direct_operator = {
        prev_direct: '<',
        next_direct: '>',
    }

    def build_filters(self, classes=None, classes_not=None, tags=None, tags_not=None, tasks=None, tasks_not=None) -> list:
        # classes = request.query_params.get('classes')
        # classes_not = request.query_params.get('classes_not')
        # tags = request.query_params.get('tags')
        # tags_not = request.query_params.get('tags_not')
        # tasks = request.query_params.get('tasks')
        # tasks_not = request.query_params.get('tasks_not')

        if isinstance(classes, str):
            classes = classes.split(',')
        if isinstance(classes, list):
            classes = list(map(capitalize_class_name, classes))

        if isinstance(classes_not, str):
            classes_not = classes_not.split(',')
        if isinstance(classes_not, list):
            classes_not = list(map(capitalize_class_name, classes_not))

        if isinstance(tags, str):
            tags = tags.split(',')

        if isinstance(tags_not, str):
            tags_not = tags_not.split(',')

        if isinstance(tasks, str):
            tasks = tasks.split(',')
        if isinstance(tasks, list):
            # allowed only one task
            task = parse_annotation_task(tasks[0])
            tasks = [task.name] if task else []

        if isinstance(tasks_not, str):
            tasks_not = tasks_not.split(',')
        if isinstance(tasks_not, list):
            # allowed only one task
            task = parse_annotation_task(tasks_not[0])
            tasks_not = [task.name] if task else []

        filters = []
        if classes:
            for name in classes:
                filters.append({
                    'name': 'class',
                    'condition': 'is',
                    'pattern': name,
                })

        if classes_not:
            for name in classes_not:
                filters.append({
                    'name': 'class',
                    'condition': 'is_not',
                    'pattern': name,
                })

        if tags:
            for name in tags:
                filters.append({
                    'name': 'tag',
                    'condition': 'is',
                    'pattern': name,
                })

        if tags_not:
            for name in tags_not:
                filters.append({
                    'name': 'tag',
                    'condition': 'is_not',
                    'pattern': name,
                })
        if tasks:
            for name in tasks:
                filters.append({
                    'name': 'task',
                    'condition': 'is',
                    'pattern': name,
                })

        if tasks_not:
            for name in tasks_not:
                filters.append({
                    'name': 'task',
                    'condition': 'is_not',
                    'pattern': name,
                })

        return filters


    def execute(self, dataset_id=None, image_id=None, direction=None, limit=None, classes=None, classes_not=None, tags=None, tags_not=None, tasks=None, tasks_not=None):
        filters = self.build_filters(classes, classes_not, tags, tags_not, tasks, tasks_not)

        qb = QueryBuilder("SELECT id FROM new_annotations")

        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        if image_id:
            comparison = self.direct_operator.get(direction)
            qb.condition(QueryBuilder.Condition("image_id", comparison, image_id))

        for filter in filters:
            qb.condition(transform_filter_to_condition(filter))

        qb.order_by("image_id")
        qb.limit(limit + 1)

        return NewAnnotation.objects.raw(qb.query())
        # data = self._query_data(qb.query())
        # resp = self._paginate_resp(data, limit, image_id, direction)
        # return Response(resp)

    # @staticmethod
    # def _parse_int_param(value, default=None, min_value: int = None):
    #     if value:
    #         try:
    #             value = int(value)
    #             if min_value:
    #                 value = max(value, min_value)
    #         except ValueError:
    #             value = default
    #     return value
    #
    # def _query_data(self, query):
    #     page = NewAnnotation.objects.raw(query)
    #     serializer = self.get_serializer(page, many=True)
    #     return serializer.data
    #
    # def _paginate_resp(self, data, limit, image_id, direction):
    #     next_url = None
    #     prev_url = None
    #     left, right = 0, len(data)
    #     if len(data) > limit:
    #         image_index = self._get_image_index(data, image_id)
    #         left, right = self.filter_range(image_index, limit, len(data))
    #
    #     if left > 0 and direction != self.next_direct:
    #         prev_url = self._create_url(data[left]['image_id'], self.prev_direct)
    #     if right < len(data) and direction != self.prev_direct:
    #         next_url = self._create_url(data[right - 1]['image_id'], self.next_direct)
    #
    #     results = data[left:right]
    #
    #     return {
    #         'count': len(results),
    #         'next': next_url,
    #         'previous': prev_url,
    #         'results': results
    #     }
    #
    # def _create_url(self, img_id, direction):
    #     current_url = self.request.get_full_path()
    #     url = replace_query_param(current_url, 'image_id', img_id)
    #     return replace_query_param(url, 'direction', direction)
    #
    # @staticmethod
    # def _get_image_index(data, image_id):
    #     if not image_id:
    #         return
    #
    #     for index, img in enumerate(data):
    #         if img['image_id'] >= image_id:
    #             return index
    #
    # @staticmethod
    # def filter_range(img_idx: int, limit: int, size: int):
    #     if img_idx is None:
    #         return 0, limit
    #
    #     half = int(limit / 2)
    #     left = img_idx - half
    #     right = img_idx + limit - half
    #
    #     if left < 0:
    #         rest = -left
    #         left = 0
    #         right += rest
    #     elif right > size:
    #         rest = right - size
    #         right = size
    #         left -= rest
    #
    #     return left, right
