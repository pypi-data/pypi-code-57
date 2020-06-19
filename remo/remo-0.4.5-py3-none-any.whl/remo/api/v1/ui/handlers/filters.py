from django.conf import settings
from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.utils.urls import replace_query_param

from remo_app.remo.models import DatasetImage
from remo_app.remo.use_cases.classes import capitalize_class_name
from remo_app.remo.use_cases.query_builder import QueryBuilder, transform_filter_to_condition


class ImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='original_name')
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = DatasetImage
        fields = ('id', 'name', 'thumbnail')

    def get_thumbnail(self, instance):
        return instance.image_object.thumbnail.url if instance.image_object.thumbnail else None


class Filters(viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    ordering = 'id'
    prev_direct = 'prev'
    next_direct = 'next'
    direct_name = 'direction'
    direct_operator = {
        prev_direct: '<',
        next_direct: '>',
    }

    def list(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    @staticmethod
    def _parse_int_param(value, default=None, min_value: int = None):
        if value is None:
            return None

        try:
            value = int(value)
            if min_value:
                value = max(value, min_value)
        except ValueError:
            value = default
        return value

    def _query_data(self, query):
        page = DatasetImage.objects.raw(query)
        serializer = self.get_serializer(page, many=True)
        return serializer.data

    def _query_count(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            count = cursor.fetchone()[0]
        return count

    def _images_in_direction(self, direction, dataset_id, image_id, folder_id, limit, equal=False):
        qb = QueryBuilder("SELECT id, original_name FROM dataset_images")
        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        if folder_id:
            qb.condition(QueryBuilder.Condition("folder_id", "=", folder_id))

        if image_id:
            comparison = self.direct_operator.get(direction)
            if equal:
                comparison += "="
            qb.condition(QueryBuilder.Condition("id", comparison, image_id))

        order_direction = 'DESC' if direction == self.prev_direct else 'ASC'
        qb.order_by("id", order_direction)
        qb.limit(limit + 1)
        data = self._query_data(qb.query())

        if direction == self.prev_direct:
            data.reverse()

        return data

    def _count_images(self, dataset_id, folder_id):
        qb = QueryBuilder("SELECT COUNT(id) FROM dataset_images")
        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        if folder_id:
            qb.condition(QueryBuilder.Condition("folder_id", "=", folder_id))

        # TODO: count for images in nested folders

        return self._query_count(qb.query())

    def _images(self, dataset_id, image_id, folder_id, limit):
        if image_id:
            next = self._images_in_direction(self.next_direct, dataset_id, image_id, folder_id, limit, equal=True)
            prev = self._images_in_direction(self.prev_direct, dataset_id, image_id, folder_id, limit)
            return prev + next

        return self._images_in_direction(self.next_direct, dataset_id, image_id, folder_id, limit)

    def _filter_image_ids_in_direction(self, filters, direction, dataset_id, image_id, limit, equal=False):
        qb = QueryBuilder("SELECT DISTINCT image_id FROM new_annotations")

        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        if image_id:
            comparison = self.direct_operator.get(direction)
            if equal:
                comparison += "="
            qb.condition(QueryBuilder.Condition("image_id", comparison, image_id))

        for filter in filters:
            qb.condition(transform_filter_to_condition(filter))

        order_direction = 'DESC' if direction == self.prev_direct else 'ASC'
        qb.order_by("image_id", order_direction)
        qb.limit(limit + 1)

        query = qb.query()
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        return [id[0] for id in ids]

    def _count_filtered_images(self, filters, dataset_id):
        qb = QueryBuilder("SELECT COUNT(DISTINCT image_id) FROM new_annotations")

        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        for filter in filters:
            qb.condition(transform_filter_to_condition(filter))

        return self._query_count(qb.query())

    def _filter_image_ids(self, filters, dataset_id, image_id, limit):
        if image_id:
            next = self._filter_image_ids_in_direction(filters, self.next_direct, dataset_id, image_id, limit, equal=True)
            prev = self._filter_image_ids_in_direction(filters, self.prev_direct, dataset_id, image_id, limit)
            return prev + next

        return self._filter_image_ids_in_direction(filters, self.next_direct, dataset_id, image_id, limit)

    def get_images(self, direction, dataset_id, image_id, folder_id, limit):
        if direction:
            data = self._images_in_direction(direction, dataset_id, image_id, folder_id, limit)
        else:
            data = self._images(dataset_id, image_id, folder_id, limit)

        count = self._count_images(dataset_id, folder_id)
        return data, count

    def get_filtered_images(self, filters, direction, dataset_id, image_id, limit):
        if direction:
            ids = self._filter_image_ids_in_direction(filters, direction, dataset_id, image_id, limit)
        else:
            ids = self._filter_image_ids(filters, dataset_id, image_id, limit)

        if len(ids) == 0:
            return [], 0

        ids = ", ".join(map(str, ids))
        query = "SELECT id, original_name FROM dataset_images WHERE id IN ({})".format(ids)
        data = self._query_data(query)

        count = self._count_filtered_images(filters, dataset_id)
        return data, count

    def post(self, request, *args, **kwargs):
        filters = request.data.get('filters', [])
        for f in filters:
            if f['name'] == 'class':
                f['pattern'] = capitalize_class_name(f['pattern'])

        dataset_id = self._parse_int_param(request.query_params.get('dataset_id'), min_value=1)
        folder_id = self._parse_int_param(request.query_params.get('folder_id'), min_value=1)
        image_id = self._parse_int_param(request.query_params.get('image_id'), min_value=1)
        default_limit = settings.REST_FRAMEWORK['PAGE_SIZE']
        limit = self._parse_int_param(request.query_params.get('limit', default_limit), default_limit, 1)
        direction = request.query_params.get(self.direct_name)

        if image_id:
            img = DatasetImage.objects.filter(id=image_id).first()
            if img:
                folder_id = img.folder_id

        if not len(filters):
            data, total_count = self.get_images(direction, dataset_id, image_id, folder_id, limit)
        else:
            data, total_count = self.get_filtered_images(filters, direction, dataset_id, image_id, limit)

        resp = self._paginate_resp(data, total_count, limit, image_id, direction)
        return Response(resp)

    def _paginate_resp(self, data, total_count, limit, image_id, direction):
        next_url = None
        prev_url = None
        left, right = 0, len(data)
        if len(data) > limit:
            if image_id:
                image_index = self._get_image_index(data, image_id)
                left, right = self.filter_range(image_index, limit, len(data))
            else:
                right = limit

        if left > 0 and direction != self.next_direct:
            prev_url = self._create_url(data[left]['id'], self.prev_direct)
        if right < len(data) and direction != self.prev_direct:
            next_url = self._create_url(data[right - 1]['id'], self.next_direct)

        results = data[left:right]

        return {
            'count': len(results),
            'total_count': total_count,
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
        for index, img in enumerate(data):
            if img['id'] >= image_id:
                return index

    @staticmethod
    def filter_range(img_idx: int, limit: int, size: int):
        if img_idx is None:
            return size - limit, size

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
