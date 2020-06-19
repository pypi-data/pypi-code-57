import logging
from itertools import chain

from django.db import connection
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseForbidden
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param

from remo_app.remo.models import Annotation, AnnotationSet
from remo_app.remo.api.constants import TaskType, default_status, AnnotationStatus
from remo_app.remo.api.views.mixins import DestroyImageModelMixin
from remo_app.remo.api.serializers import (
    AnnotationSetDatasetImageSerializer,
    CommonClassSerializer,
    AnnotationCreateUpdateClassSerializer,
    AnnotationCreateUpdateObjectSerializer
)
from remo_app.remo.api.viewsets import BaseGrandNestedModelViewSet
from remo_app.remo.models.annotation import Tracker
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.models import Dataset, DatasetImage
from remo_app.remo.use_cases.annotation import update_new_annotation
import functools, operator

logger = logging.getLogger('remo_app')


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class DatasetAnnotationSetImageFilterSet(FilterSet):
    tags_in = CharInFilter(field_name='tag__name', distinct=True)
    classes_in = CharInFilter(method='classes_in_filter')

    def classes_in_filter(self, qs, name, value):
        return qs.filter(
            Q(  # Image classification
                annotations__classes__name__in=value
            ) | Q(  # Object detection/object segmentation
                annotations__annotation_objects__classes__name__in=value
            )
        ).distinct()

    class Meta:
        model = DatasetImage
        fields = ('classes_in', 'tags_in')


class DatasetAnnotationSetImageViewSet(
    mixins.RetrieveModelMixin,
    DestroyImageModelMixin,
    BaseGrandNestedModelViewSet):
    grand_parent_lookup = 'dataset'
    parent_lookup = 'annotation_set'
    serializer_class = AnnotationSetDatasetImageSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = 'id'
    prev_direct = 'prev'
    next_direct = 'next'
    direct_name = 'direction'
    direct_operator = {
        prev_direct: '<',
        next_direct: '>',
    }

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

    def _get_tracker(self, id):
        tracker = Tracker.objects.filter(id=id).first()
        if not tracker:
            tracker = Tracker(gallery=[])
        return tracker

    def list(self, request, *args, **kwargs):
        folder_id = self._parse_int_param(request.query_params.get('folder_id'), min_value=1)
        image_id = self._parse_int_param(request.query_params.get('image_id'), min_value=1)
        tracker_id = self._parse_int_param(request.query_params.get('tracker_id'), min_value=1)

        order = request.query_params.get('order', 'not_annotated')
        default_limit = settings.REST_FRAMEWORK['PAGE_SIZE']
        limit = self._parse_int_param(request.query_params.get('limit', default_limit), default_limit, 1)
        direction = request.query_params.get(self.direct_name)

        queryset = self.filter_queryset(self.get_queryset())

        # TODO: TBD
        # if image_id and not folder_id:
        #     img = DatasetImage.objects.filter(id=image_id).first()
        #     if img:
        #         folder_id = img.folder_id
        # queryset = queryset.filter(folder_id=folder_id)

        if tracker_id:
            if image_id and direction:
                return self._image_fllow_next(order, queryset, limit, image_id, tracker_id, direction)
            else:
                return self._basic_flow_next(order, queryset, limit, tracker_id)

        if image_id:
            return self._image_flow_init(order, queryset, limit, image_id)
        else:
            return self._basic_flow_init(order, queryset, limit)

    def _image_fllow_next(self, order, queryset, limit, image_id, tracker_id, direction):
        tracker = self._get_tracker(tracker_id)
        gallery = set(tracker.gallery)
        g = gallery.copy()
        g.remove(image_id)
        g = list(g)

        ordered_images, counts = self._order_images_with_not_in(order, queryset, image_id, limit + 2, g)
        next_imgs = []
        prev_imgs = []
        found_img = False

        for img in ordered_images:
            if not found_img and img == image_id:
                found_img = True

            if img in gallery:
                continue

            if not found_img:
                prev_imgs.append(img)
            else:
                next_imgs.append(img)

            if len(next_imgs) > limit + 1:
                break

        next_imgs = next_imgs[:limit + 1]
        prev_imgs = prev_imgs[-(limit + 1):]

        if direction == self.next_direct:
            result = next_imgs
        elif direction == self.prev_direct:
            result = prev_imgs

        has_prev, has_next = False, False

        q = list(DatasetImage.objects.filter(pk__in=result))
        q.sort(key=lambda t: result.index(t.pk))

        serializer = self.get_serializer(q, many=True)
        data = serializer.data

        if len(data) > limit:
            if direction == self.next_direct:
                has_next = True
                data = data[:-1]
            elif direction == self.prev_direct:
                has_prev = True
                data = data[1:]

        for img in data:
            gallery.add(img['id'])

        tracker.gallery = list(gallery)
        tracker.save()

        return Response(self._paginate_resp_with_image(counts, data, image_id, tracker.id, has_prev, has_next))

    def _image_flow_init(self, order, queryset, limit, image_id):
        ordered_images, counts = self._order_images_for_image(order, queryset, limit + 2, image_id)
        next_imgs = []
        prev_imgs = []
        found_img = False
        for img in ordered_images:
            if not found_img and img == image_id:
                found_img = True

            if not found_img:
                prev_imgs.append(img)
            else:
                next_imgs.append(img)

            if len(next_imgs) > limit:
                break

        next_imgs = next_imgs[:limit]
        prev_imgs = prev_imgs[-limit:]

        result = prev_imgs + next_imgs
        has_prev, has_next = False, False

        q = list(DatasetImage.objects.filter(pk__in=result))
        q.sort(key=lambda t: result.index(t.pk))

        serializer = self.get_serializer(q, many=True)
        data = serializer.data
        n = len(data)
        if n > limit:
            image_index = self._get_target_image_index(data, image_id)
            left, right = self.filter_range(image_index, limit, n)

            has_prev = (left > 0)
            has_next = (right < n - 1)
            data = data[left:right]

        tracker = Tracker(gallery=list(map(lambda img: img['id'], data)))
        tracker.save()

        return Response(self._paginate_resp_with_image(counts, data, image_id, tracker.id, has_prev, has_next))

    def _basic_flow_next(self, order, queryset, limit, tracker_id):
        tracker = self._get_tracker(tracker_id)
        gallery = set(tracker.gallery)

        imgs, counts = self._order_images(order, queryset, limit + 1, tracker.gallery)

        result = []
        for img in imgs:
            if img in gallery:
                continue

            result.append(img)
            if len(result) > limit:
                break

        q = list(DatasetImage.objects.filter(pk__in=result))
        q.sort(key=lambda t: result.index(t.pk))

        serializer = self.get_serializer(q, many=True)
        data = serializer.data

        has_next = False
        if len(data) > limit:
            has_next = True
            data = data[:-1]

        for img in data:
            gallery.add(img['id'])

        tracker.gallery = list(gallery)
        tracker.save()

        return Response(self._basic_paginate_resp(counts, data, tracker.id, has_next))

    def _basic_flow_init(self, order, queryset, limit):
        ordered_images, counts = self._order_images(order, queryset, limit + 1)
        result = []
        for img in ordered_images:
            result.append(img)
            if len(result) == limit + 1:
                break

        has_next = False
        if len(result) > limit:
            has_next = True
            result = result[:-1]

        tracker = Tracker(gallery=result)
        tracker.save()

        q = list(DatasetImage.objects.filter(pk__in=result))
        q.sort(key=lambda t: result.index(t.pk))

        serializer = self.get_serializer(q, many=True)
        data = serializer.data
        return Response(self._basic_paginate_resp(counts, data, tracker.id, has_next))

    def _order_images_for_image(self, order, queryset, limit, image_id):
        annotation_set = self.get_parent_object_or_404()
        dataset_id = annotation_set.dataset.id
        annotation_set_id = annotation_set.id

        skipped = self._query_annotated_images_for_image(dataset_id, annotation_set_id, 0, limit, image_id)
        annotated = self._query_annotated_images_for_image(dataset_id, annotation_set_id, 1, limit, image_id)
        not_annotated = self._query_images_for_image(dataset_id, skipped + annotated, limit, image_id)

        annotated_count = self._count_annotated_images(dataset_id, annotation_set_id, 1)
        skipped_count = self._count_annotated_images(dataset_id, annotation_set_id, 0)
        not_annotated_count = annotation_set.dataset.quantity - annotated_count - skipped_count

        # print(
        #     'not_annotated:', not_annotated_count, '\t', not_annotated, '\n',
        #     'skipped:      ', skipped_count, '\t', skipped, '\n',
        #     'annotated:    ', annotated_count, '\t', annotated
        # )

        if order == 'not_annotated':
            in_order = chain(not_annotated, skipped, annotated)
        elif order == 'skipped':
            in_order = chain(skipped, not_annotated, annotated)
        elif order == 'annotated':
            in_order = chain(annotated, skipped, not_annotated)
        else:
            in_order = queryset

        return in_order, (not_annotated_count, skipped_count, annotated_count)

    def _order_images_with_not_in(self, order, queryset, image_id, limit=32, gallery=[]):
        annotation_set = self.get_parent_object_or_404()
        dataset_id = annotation_set.dataset.id
        annotation_set_id = annotation_set.id

        skipped = self._query_annotated_images_for_image_with_not_in(dataset_id, annotation_set_id, 0, limit, image_id,
                                                                     gallery)
        annotated = self._query_annotated_images_for_image_with_not_in(dataset_id, annotation_set_id, 1, limit,
                                                                       image_id, gallery)
        not_annotated = self._query_images_for_image(dataset_id, gallery + skipped + annotated, limit, image_id)

        annotated_count = self._count_annotated_images(dataset_id, annotation_set_id, 1)
        skipped_count = self._count_annotated_images(dataset_id, annotation_set_id, 0)
        not_annotated_count = annotation_set.dataset.quantity - annotated_count - skipped_count

        # print(
        #     'not_annotated:', not_annotated_count, '\t', not_annotated, '\n',
        #     'skipped:      ', skipped_count, '\t', skipped, '\n',
        #     'annotated:    ', annotated_count, '\t', annotated
        # )

        if order == 'not_annotated':
            in_order = chain(not_annotated, skipped, annotated)
        elif order == 'skipped':
            in_order = chain(skipped, not_annotated, annotated)
        elif order == 'annotated':
            in_order = chain(annotated, skipped, not_annotated)
        else:
            in_order = queryset

        return in_order, (not_annotated_count, skipped_count, annotated_count)

    def _order_images(self, order, queryset, limit=32, gallery=[]):
        annotation_set = self.get_parent_object_or_404()
        dataset_id = annotation_set.dataset.id
        annotation_set_id = annotation_set.id

        skipped = self._query_annotated_images(dataset_id, annotation_set_id, 0, gallery, limit)
        annotated = self._query_annotated_images(dataset_id, annotation_set_id, 1, gallery, limit)
        not_annotated = self._query_not_annotated_images(dataset_id, annotation_set_id, gallery, limit)
        # not_annotated = list(set(images) - set(annotated) - set(skipped))

        # annotated = queryset.filter(new_annotations__annotation_set=annotation_set, new_annotations__status=1)
        # skipped = queryset.filter(new_annotations__annotation_set=annotation_set, new_annotations__status=0)
        # not_annotated = queryset.difference(annotated, skipped)

        # annotated_count = 0  # annotated.count()
        # skipped_count = 0  # skipped.count()
        # not_annotated_count = not_annotated.count()
        annotated_count = self._count_annotated_images(dataset_id, annotation_set_id, 1)
        skipped_count = self._count_annotated_images(dataset_id, annotation_set_id, 0)
        not_annotated_count = annotation_set.dataset.quantity - annotated_count - skipped_count

        # print(
        #     'not_annotated:', not_annotated_count, '\t', not_annotated, '\n',
        #     'skipped:      ', skipped_count, '\t', skipped, '\n',
        #     'annotated:    ', annotated_count, '\t', annotated
        # )

        if order == 'not_annotated':
            in_order = chain(not_annotated, skipped, annotated)
        elif order == 'skipped':
            in_order = chain(skipped, not_annotated, annotated)
        elif order == 'annotated':
            in_order = chain(annotated, skipped, not_annotated)
        else:
            in_order = queryset

        return in_order, (not_annotated_count, skipped_count, annotated_count)

    def _query_annotated_images(self, dataset_id, annotation_set_id, status, not_in, limit):
        skip_ids = ""
        if len(not_in):
            skip_ids = """ AND "dataset_images"."id" NOT IN ({skipped}) """.format(skipped=",".join(map(str, not_in)))

        query = """
                SELECT "dataset_images"."id"
                FROM "dataset_images"
                INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
                WHERE ("dataset_images"."dataset_id" = {dataset_id}
                        AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                        AND "new_annotations"."status" = {status})
                        {skip_ids}
                ORDER BY "dataset_images"."id" ASC
                LIMIT {limit}
                """.format(
            dataset_id=dataset_id,
            annotation_set_id=annotation_set_id,
            status=status,
            skip_ids=skip_ids,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        ids = [id[0] for id in ids]
        return ids
        # return DatasetImage.objects.raw(query)

    def _query_annotated_images_for_image(self, dataset_id, annotation_set_id, status, limit, image_id):
        query = """
                SELECT "dataset_images"."id"
                FROM "dataset_images"
                INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
                WHERE ("dataset_images"."dataset_id" = {dataset_id}
                        AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                        AND "new_annotations"."status" = {status})
                        AND "dataset_images"."id" < {image_id}
                ORDER BY "dataset_images"."id" ASC
                LIMIT {limit}
                """.format(
            dataset_id=dataset_id,
            annotation_set_id=annotation_set_id,
            status=status,
            image_id=image_id,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        prev = [id[0] for id in ids]

        query = """
                        SELECT "dataset_images"."id"
                        FROM "dataset_images"
                        INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
                        WHERE ("dataset_images"."dataset_id" = {dataset_id}
                                AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                                AND "new_annotations"."status" = {status})
                                AND "dataset_images"."id" >= {image_id}
                        ORDER BY "dataset_images"."id" ASC
                        LIMIT {limit}
                        """.format(
            dataset_id=dataset_id,
            annotation_set_id=annotation_set_id,
            status=status,
            image_id=image_id,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        next = [id[0] for id in ids]
        return prev + next

    def _query_annotated_images_for_image_with_not_in(self, dataset_id, annotation_set_id, status, limit, image_id,
                                                      not_in=[]):
        skip_ids = ""
        if len(not_in):
            skip_ids = """ AND "dataset_images"."id" NOT IN ({skipped}) """.format(skipped=",".join(map(str, not_in)))

        query = """
                SELECT "dataset_images"."id"
                FROM "dataset_images"
                INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
                WHERE ("dataset_images"."dataset_id" = {dataset_id}
                        AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                        AND "new_annotations"."status" = {status})
                        AND "dataset_images"."id" < {image_id}
                        {skip_ids}
                ORDER BY "dataset_images"."id" ASC
                LIMIT {limit}
                """.format(
            dataset_id=dataset_id,
            annotation_set_id=annotation_set_id,
            status=status,
            image_id=image_id,
            skip_ids=skip_ids,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        prev = [id[0] for id in ids]

        query = """
                        SELECT "dataset_images"."id"
                        FROM "dataset_images"
                        INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
                        WHERE ("dataset_images"."dataset_id" = {dataset_id}
                                AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                                AND "new_annotations"."status" = {status})
                                AND "dataset_images"."id" >= {image_id}
                                {skip_ids}
                        ORDER BY "dataset_images"."id" ASC
                        LIMIT {limit}
                        """.format(
            dataset_id=dataset_id,
            annotation_set_id=annotation_set_id,
            status=status,
            image_id=image_id,
            skip_ids=skip_ids,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        next = [id[0] for id in ids]
        return prev + next

    def _query_not_annotated_images(self, dataset_id, annotation_set_id, not_in, limit):
        skip_ids = ""
        if len(not_in):
            skip_ids = """ AND "id" NOT IN ({skipped}) """.format(skipped=",".join(map(str, not_in)))

        query = f"""
        SELECT id
        FROM dataset_images
        WHERE dataset_id = {dataset_id}
          AND id NOT IN (
            SELECT "dataset_images"."id"
            FROM "dataset_images"
                     INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
            WHERE ("dataset_images"."dataset_id" = {dataset_id}
                AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                AND "new_annotations"."status" >= 0)
        ) {skip_ids}
        ORDER BY "id" ASC
        LIMIT {limit}
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        ids = [id[0] for id in ids]
        return ids

    def _query_images_for_image(self, dataset_id, not_in, limit, image_id):
        skip_ids = ""
        if len(not_in):
            skip_ids = """ AND "id" NOT IN ({skipped}) """.format(skipped=",".join(map(str, not_in)))

        query = """
                SELECT "id"
                FROM "dataset_images"
                WHERE "dataset_id" = {dataset_id} {skip_ids} AND "id" < {image_id}
                ORDER BY "id" ASC
                LIMIT {limit}
                """.format(
            dataset_id=dataset_id,
            skip_ids=skip_ids,
            image_id=image_id,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        prev = [id[0] for id in ids]

        query = """
                        SELECT "id"
                        FROM "dataset_images"
                        WHERE "dataset_id" = {dataset_id} {skip_ids} AND "id" >= {image_id}
                        ORDER BY "id" ASC
                        LIMIT {limit}
                        """.format(
            dataset_id=dataset_id,
            skip_ids=skip_ids,
            image_id=image_id,
            limit=limit
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        next = [id[0] for id in ids]

        return prev + next

    def _count_annotated_images(self, dataset_id, annotation_set_id, status):
        query = """
                SELECT COUNT("dataset_images"."id") as count
                FROM "dataset_images"
                INNER JOIN "new_annotations" ON ("dataset_images"."id" = "new_annotations"."image_id")
                WHERE ("dataset_images"."dataset_id" = {dataset_id}
                        AND "new_annotations"."annotation_set_id" = {annotation_set_id}
                        AND "new_annotations"."status" = {status})
                """.format(
            dataset_id=dataset_id,
            annotation_set_id=annotation_set_id,
            status=status
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            count = cursor.fetchone()[0]
        return count

    def _paginate_resp_with_image(self, counts, data, image_id, tracker_id, has_prev=False, has_next=False):
        next_url = None
        prev_url = None

        if has_next:
            next_url = self._new_create_url(image_id, self.next_direct, tracker_id)

        if has_prev:
            prev_url = self._new_create_url(image_id, self.prev_direct, tracker_id)

        not_annotated_count, skipped_count, annotated_count = counts
        count = not_annotated_count + skipped_count + annotated_count

        return {
            'count': count,
            'not_annotated_count': not_annotated_count,
            'skipped_count': skipped_count,
            'annotated_count': annotated_count,
            'next': next_url,
            'previous': prev_url,
            'results': data
        }

    def _new_paginate_resp(self, counts, data, limit, image_id, direction, tracker_id, has_prev=False, has_next=False):
        next_url = None
        prev_url = None
        # left, right = 0, len(data)
        # if len(data) > limit:
        #     image_index = self._get_image_index(data, image_id)
        #     left, right = self.filter_range(image_index, limit, len(data))
        #
        # if left > 0 and direction != self.next_direct:
        #     prev_url = self._create_url(data[left]['id'], self.prev_direct)
        #
        # if right < len(data) and direction != self.prev_direct:
        #     next_url = self._create_url(data[right - 1]['id'], self.next_direct)
        # if direction != self.prev_direct and len(data) > limit:
        if has_next:
            next_url = self._new_create_url(data[-1]['id'], self.next_direct, tracker_id)
            # data = data[:-1]

        if has_prev:
            prev_url = self._new_create_url(data[0]['id'], self.prev_direct, tracker_id)

        # results = data[left:right]

        not_annotated_count, skipped_count, annotated_count = counts
        count = not_annotated_count + skipped_count + annotated_count

        return {
            'count': count,
            'not_annotated_count': not_annotated_count,
            'skipped_count': skipped_count,
            'annotated_count': annotated_count,
            'next': next_url,
            'previous': prev_url,
            'results': data
        }

    def _basic_paginate_resp(self, counts, data, tracker_id, has_next=False):
        next_url = None
        prev_url = None
        if has_next:
            next_url = self._basic_create_url(self.next_direct, tracker_id)

        not_annotated_count, skipped_count, annotated_count = counts
        count = not_annotated_count + skipped_count + annotated_count

        return {
            'count': count,
            'not_annotated_count': not_annotated_count,
            'skipped_count': skipped_count,
            'annotated_count': annotated_count,
            'next': next_url,
            'previous': prev_url,
            'results': data
        }

    def _paginate_resp(self, count, data, limit, image_id, direction):
        next_url = None
        prev_url = None
        left, right = 0, len(data)
        if len(data) > limit:
            image_index = self._get_image_index(data, image_id)
            left, right = self.filter_range(image_index, limit, len(data))

        if left > 0 and direction != self.next_direct:
            prev_url = self._create_url(data[left]['id'], self.prev_direct)
        if right < len(data) and direction != self.prev_direct:
            next_url = self._create_url(data[right - 1]['id'], self.next_direct)

        results = data[left:right]

        return {
            'count': count,
            'next': next_url,
            'previous': prev_url,
            'results': results
        }

    def _create_url(self, img_id, direction):
        current_url = self.request.get_full_path()
        url = replace_query_param(current_url, 'image_id', img_id)
        return replace_query_param(url, 'direction', direction)

    def _new_create_url(self, img_id, direction, tracker_id):
        current_url = self.request.get_full_path()
        url = replace_query_param(current_url, 'image_id', img_id)
        url = replace_query_param(url, 'direction', direction)
        return replace_query_param(url, 'tracker_id', tracker_id)

    def _basic_create_url(self, direction, tracker_id):
        current_url = self.request.get_full_path()
        url = replace_query_param(current_url, 'direction', direction)
        return replace_query_param(url, 'tracker_id', tracker_id)

    @staticmethod
    def _get_image_index(data, image_id):
        if not image_id:
            return None
        for index, img in enumerate(data):
            if img['id'] >= image_id:
                return index

    @staticmethod
    def _get_target_image_index(data, image_id):
        for index, img in enumerate(data):
            if img['id'] == image_id:
                return index

    @staticmethod
    def filter_range(img_idx: int, limit: int, size: int):
        if img_idx is None:
            return 0, limit
            # return size - limit, size

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

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)

        # RDF's FilterSet can't combine several filters via OR
        # without bunch of hacks. Therefore its better do it by hand
        # (query_parameter, queryset_field)
        fields = (
            ('tags_in', 'tag__name__in'),
            ('classes_in', 'annotations__classes__name__in'),
            ('classes_in', 'annotations__annotation_objects__classes__name__in')
        )

        fltr = []
        for param, qsfield in fields:
            query = self.request.query_params.get(param)
            if query:
                splitted = query.split(',')
                fltr.append(Q(**{qsfield: splitted}))

        if fltr:
            qs = qs.filter(functools.reduce(operator.or_, fltr))

        return qs

    def get_grand_parent_queryset(self):
        return Dataset.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def get_parent_queryset(self):
        dataset = self.get_grand_parent_object_or_404()
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True), dataset=dataset)

    def get_queryset(self):
        annotation_set = self.get_parent_object_or_404()
        return DatasetImage.objects.filter(dataset=annotation_set.dataset)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['dataset'] = self.get_grand_parent_object_or_404()
        ctx['annotation_set'] = self.get_parent_object_or_404()
        return ctx

    # TODO: Vova, check if we still use this
    @action(['get'], detail=True, url_path='annotation')
    def get_annotated_data(self, request, *args, **kwargs):
        dataset_image = self.get_object()
        annotation_set = self.get_parent_object_or_404()
        task = annotation_set.task

        # serializer based on annotation set's task type
        serializer_class = (AnnotationCreateUpdateClassSerializer
                            if task.type == TaskType.image_classification.name
                            else AnnotationCreateUpdateObjectSerializer)

        # return saved data from db (continue annotation)
        qs = Annotation.objects.filter(image=dataset_image, annotation_set=annotation_set)
        if qs.count() > 1:  # FIXME: always False, see Annotation.unique_together
            logger.error(
                'More than 1 annotations for DatasetImage #{}, AnnotationSet #{}. Use first'.format(
                    dataset_image.id, annotation_set.pk
                )
            )
        if qs:
            annotation = qs.first()
            annotation_info = serializer_class(annotation, context=self.get_serializer_context()).data['annotation_info']

            return Response({
                'error': False,
                'annotation_info': annotation_info,
                'status': AnnotationStatus(annotation.status).name
            })

        if not task or task.type == TaskType.image_classification:
            return Response({'error': False, 'annotation_info': [], 'status': default_status.name})

        # filename = os.path.basename(dataset_image.image_object.image.name)
        # path_to_image = 'dataset_images/{}'.format(filename)
        # image_content = get_image_content(path_to_image)
        # url = 'http://{}:{}/recognize'.format(annotation_set.model.url, annotation_set.model.port)
        #
        # retry_counts = settings.MODEL_CONNECTION_RETRY_COUNTS
        # while retry_counts > 0:
        #     try:
        #         r = requests.post(url, data={'key': 'sosecretnow'}, files={'file': image_content})
        #         response = r.json()
        #         retry_counts = 0
        #     except requests.exceptions.ConnectionError:
        #         retry_counts -= 1
        #         logger.warning('Cannot connect to API. Retry counts: {}'.format(retry_counts))
        #         time.sleep(settings.MODEL_CONNECTION_RETRY_TIMEOUT)
        #         if not retry_counts:
        #             return Response({
        #                 'error': 'Connection to models API was refused',
        #                 'annotation_info': [],
        #                 'skipped': None
        #             })
        #     except json.decoder.JSONDecodeError:
        #         logger.error('Cannot decode json for image {}. '
        #                      'Response from model API: {}'.format(dataset_image.id, r.content))
        #         return Response({'error': False, 'annotation_info': [], 'skipped': False})
        # if 'error' in response:
        #     return Response(response)

        annotation_set_classes = {cls.name.lower(): cls for cls in annotation_set.classes.all()}

        annotations = []
        # todo: add normal serializer in future
        if task.available_tools.filter(code_name='rectangle').count():
            serializer = self.rectangle_serializer
        else:
            serializer = self.polygon_serializer

        # for annotation_object in response:
        #     common_class_name = annotation_object['class'].lower()
        #     annotation_set_class = annotation_set_classes.get(common_class_name)
        #     if not annotation_set_class:
        #         continue
        #
        #     is_questionable = annotation_object['score'] < annotation_set.model.questionable_boundary
        #
        #     annotations.append(serializer(annotation_object, annotation_set_class, is_questionable))

        return Response({'error': False, 'annotation_info': annotations, 'status': default_status.name})

    def polygon_serializer(self, annotation_object, annotation_set_class, is_questionable):
        return {
            'classes': [{
                **CommonClassSerializer(annotation_set_class).data,
                **{
                    'score': round(annotation_object['score'], 2),
                    'questionable': is_questionable
                }
            }],
            'coordinates': [
                {
                    'x': object_item[0],
                    'y': object_item[1]
                    # todo: now take [0], but it may contain more. Need ask Carlo how to process it
                } for object_item in annotation_object['coordinates'][0]
            ]
        }

    def rectangle_serializer(self, annotation_object, annotation_set_class, is_questionable):
        return {
            'classes': [{
                **CommonClassSerializer(annotation_set_class).data,
                **{
                    'score': round(annotation_object['score'], 2),
                    'questionable': is_questionable
                }
            }],
            'coordinates': [
                {
                    'x': annotation_object['coordinates'][0][0],
                    'y': annotation_object['coordinates'][0][1]
                },
                {
                    'x': annotation_object['coordinates'][1][0],
                    'y': annotation_object['coordinates'][1][1]
                }
            ]
        }

    @action(['post'], detail=True, url_path='save-annotation')
    def save_annotation(self, request, *args, **kwargs):
        dataset = self.get_grand_parent_object_or_404()
        # TODO: check shared_users
        if dataset.user != request.user:
            return Response({'error': True, 'msg': 'Operation not permitted'}, status=HttpResponseForbidden.status_code)

        image = self.get_object()
        annotation_set = self.get_parent_object_or_404()
        annotation_objects = self.request.data.get('objects', [])
        annotation_objects = self.convert_coordinates_to_integer_values(annotation_objects)
        annotation_objects = self.deduplicate_objects(annotation_objects)
        annotation_objects = self.add_position_number(annotation_objects)

        skip_new_classes = self.request.data.get('skip_new_classes', False)
        if skip_new_classes in ('true', 'True'):
            skip_new_classes = True

        annotation_classes = self.request.data.get('classes', [])
        is_image_classification = annotation_set.task.type == TaskType.image_classification.name
        annotation_info = annotation_classes if is_image_classification else annotation_objects

        status = (AnnotationStatus.by_name(self.request.data.get('status', default_status.name)))
        new_annotation_data = {
            'annotation_info': annotation_info,
            'status': status.value,
            'skip_new_classes': skip_new_classes
        }

        # serializer based on annotation set's task type
        serializer_class = (AnnotationCreateUpdateClassSerializer
                            if is_image_classification
                            else AnnotationCreateUpdateObjectSerializer)

        annotation = None
        qs = Annotation.objects.filter(image=image, annotation_set=annotation_set)
        if qs.count() > 1:
            logger.error(
                'More than 1 annotations for DatasetImage #{}, AnnotationSet #{}. Use first'.format(
                    image.id, annotation_set.pk
                )
            )
        if qs:
            annotation = qs.first()
        else:
            new_annotation_data.update({
                'image': image.id,
                'annotation_set': annotation_set.pk
            })
        serializer = serializer_class(annotation,
                                      context=self.get_serializer_context(),
                                      data=new_annotation_data,
                                      partial=annotation is not None)

        if serializer.is_valid():
            image.dataset.update()
            serializer.save()

            if not annotation:
                annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
            update_new_annotation(annotation)
            update_annotation_set_statistics(annotation_set)
            return Response(serializer.data)

        return Response(serializer.errors)

    def deduplicate_objects(self, annotation_objects):
        uniques = set()
        unique_objects = []
        for obj in annotation_objects:
            if 'coordinates' not in obj:
                unique_objects.append(obj)
                continue
            t = self.convert_coordinates_to_tuple(obj['coordinates'])
            if t in uniques:
                continue
            uniques.add(t)
            unique_objects.append(obj)
        return unique_objects

    @staticmethod
    def convert_to_tuple(p):
        return (p['x'], p['y'])

    def convert_coordinates_to_tuple(self, coordinates):
        return tuple(map(self.convert_to_tuple, coordinates))

    def convert_coordinates_to_integer_values(self, annotation_objects):
        if not (isinstance(annotation_objects, list) and len(annotation_objects) and 'coordinates' in annotation_objects[0]):
            return annotation_objects

        for obj in annotation_objects:
            if 'coordinates' not in obj:
                continue
            obj['coordinates'] = list(map(self.convert_to_integer, obj['coordinates']))
        return annotation_objects

    @staticmethod
    def convert_to_integer(p):
        return {'x': int(p['x']), 'y': int(p['y'])}

    @staticmethod
    def add_position_number(annotation_objects):
        for i, obj in enumerate(annotation_objects, start=1):
            obj['position_number'] = i
        return annotation_objects
