import logging
import threading
import time
import requests
from django.conf import settings
# from django.contrib.postgres.aggregates import ArrayAgg as OrigArrayAgg
# from django.contrib.postgres.fields import ArrayField
from django.db.models import Q
# from django_filters import filters
# from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
# import functools, operator
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from remo_app.remo.api.v1.ui.handlers.dataset_contents import DatasetImageSerializer
from remo_app.remo.models import DatasetImage
from remo_app.remo.services.vips_image import VipsImage

logger = logging.getLogger('remo_app')


# class CharInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass
#
#
# # This is a workaround to avoid forcibly cast the whole array_agg
# # result to text and following comparison in __contains lookup using
# # sql LIKE. Here we use @> op instead.
# # This is a part of Django starting from 2.1. So Django needs to get
# # upgraded
# # https://code.djangoproject.com/ticket/28038
# # Idea taken from https://github.com/django/django/commit/149061103829fb3ad74d050b4ae3cc815b2f451c
# # TODO: remove after Django get upgraded >=2.1
# class ArrayAgg(OrigArrayAgg):
#     @property
#     def output_field(self):
#         return ArrayField(self.source_expressions[0].output_field)
#
#
# class DatasetImageFilterSet(FilterSet):
#     names_in = CharInFilter(method='names_filter')
#     classes = CharInFilter(method='classes_filter')
#     tags = CharInFilter(method='tags_filter')
#     tasks = CharInFilter(method='tasks_filter')
#     users = CharInFilter(method='users_filter')
#
#     # '_not' versions of above ones
#     names_not_in = CharInFilter(method='names_not_filter')
#     classes_not = CharInFilter(method='classes_not_filter')
#     tags_not = CharInFilter(field_name='annotation_tags__tag__name', exclude=True, distinct=True)
#     tasks_not = CharInFilter(field_name='dataset__annotation_sets__task__name', exclude=True, distinct=True)
#     users_not = CharInFilter(field_name='dataset__user__username', exclude=True, distinct=True)
#
#     class Meta:
#         model = DatasetImage
#         fields = (
#             'names_in', 'classes', 'tags', 'tasks', 'users',
#             'names_not_in', 'classes_not', 'tags_not', 'tasks_not', 'users_not'
#         )
#
#     def names_filter(self, qs, name, value):
#         # Discard too short search terms
#         value = [x for x in value if len(x) >= 3]
#
#         # Apply "icontains" lookups to every value element
#         # Q(fld1__icontains=value[0]) | Q(fld1__icontains=value[1]) | Q(fld2__contains=value[0]) ...
#         return qs.filter(
#             functools.reduce(
#                 operator.or_,
#                 (
#                     Q(**{lookup: val})
#                     for lookup in (
#                     'dataset__name__icontains',
#                     'original_name__icontains',
#                     'folder__name__icontains'
#                 )
#                     for val in value
#                 )
#             )
#         )
#
#     def classes_filter(self, qs, name, value):
#         return qs.annotate(
#             classes1_arr=ArrayAgg('annotations__classes__name'),
#             classes2_arr=ArrayAgg('annotations__annotation_objects__classes__name')
#         ).filter(
#             Q(classes1_arr__contains=value) | Q(classes2_arr__contains=value)
#         )
#
#     def tags_filter(self, qs, name, value):
#         return qs.annotate(tags_arr=ArrayAgg('annotation_tags__tag__name')).filter(tags_arr__contains=value)
#
#     def tasks_filter(self, qs, name, value):
#         return qs.annotate(
#             tasks_arr=ArrayAgg('dataset__annotation_sets__task__name')
#         ).filter(
#             tasks_arr__contains=value
#         )
#
#     def users_filter(self, qs, name, value):
#         return qs.annotate(
#             users_arr=ArrayAgg('dataset__user__username')
#         ).filter(
#             users_arr__contains=value
#         )
#
#     def names_not_filter(self, qs, name, value):
#         # Discard too short search terms
#         value = [x for x in value if len(x) >= 3]
#
#         # Apply "icontains" lookups to every value element
#         # Q(fld1__icontains=value[0]) | Q(fld1__icontains=value[1]) | Q(fld2__contains=value[0]) ...
#         return qs.exclude(
#             functools.reduce(
#                 operator.or_,
#                 (
#                     Q(**{lookup: val})
#                     for lookup in (
#                     'dataset__name__icontains',
#                     'original_name__icontains',
#                     'folder__name__icontains'
#                 )
#                     for val in value
#                 )
#             )
#         )
#
#     def classes_not_filter(self, qs, name, value):
#         return qs.exclude(
#             Q(  # Image classification
#                 annotations__classes__name__in=value
#             ) | Q(  # Object detection/object segmentation
#                 annotations__annotation_objects__classes__name__in=value
#             )
#         ).distinct()


class ImageCache:
    retention_period = settings.CACHE_RETENTION_PERIOD
    images_limit = settings.CACHE_IMAGES_LIMIT

    def __init__(self):
        self.lock = threading.Lock()
        self.images = {}
        self.last_call = {}

    def _invalidation(self):
        now = time.time()

        drop_list = []
        for id, time_value in self.last_call.items():
            if now - time_value > self.retention_period:
                drop_list.append(id)

        for id in drop_list:
            del self.images[id]
            del self.last_call[id]

        if len(self.images) > self.images_limit:
            order = sorted(self.last_call.items(), key=lambda x: x[1], reverse=True)
            drop_list = order[self.images_limit:]
            for id, _ in drop_list:
                del self.images[id]
                del self.last_call[id]

    def image(self, id):
        with self.lock:

            if id in self.images:
                self.last_call[id] = time.time()
                return self.images[id]

            try:
                img = self._load_image(id)
                if img is None:
                    return
            except Exception as err:
                logger.error(err)
                return

            self.images[id] = img
            self.last_call[id] = time.time()

            self._invalidation()
            return img

    @staticmethod
    def _load_image_from_file(path):
        img = VipsImage.from_file(path)
        if img:
            return img.copy_memory()

    @staticmethod
    def _load_image_from_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            img = VipsImage.from_buffer(response.content)
            if img:
                return img.copy_memory()

        logger.error('image does not exist {} {}'.format(response.status_code, url))

    def _load_image(self, id):
        dataset_image = DatasetImage.objects.filter(id=id).first()
        if not dataset_image:
            return

        image_object = dataset_image.image_object
        if not image_object.original:
            return

        if image_object.local_image:
            return self._load_image_from_file(image_object.local_image)

        if settings.STORAGE == 'local':
            # images in media folder
            return self._load_image_from_file('{}/{}'.format(settings.MEDIA_ROOT, image_object.original))

        if settings.STORAGE == 'aws':
            return self._load_image_from_url(image_object.original.url)

        logger.error('not implemented storage settings: {}'.format(settings.STORAGE))


image_cache = ImageCache()


class Images(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    queryset = DatasetImage.objects.all()
    serializer_class = DatasetImageSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    # filter_class = DatasetImageFilterSet
    ordering = 'id'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(dataset__is_public=True) | Q(dataset__user=self.request.user))

    @staticmethod
    def _parse_int_param(value, default=None, min_value=None, max_value=None, number_type=int):
        if value:
            try:
                value = number_type(value)

                if min_value:
                    value = max(value, min_value)

                if max_value:
                    value = min(value, max_value)

                return value

            except ValueError:
                return default

        return default

    @staticmethod
    def _parse_float_param(value, default=None, min_value=None, max_value=None):
        return Images._parse_int_param(value, default=default, min_value=min_value, max_value=max_value,
                                       number_type=float)

    @action(['get'], detail=True, url_path='cache')
    def cache(self, request, pk=None):
        global image_cache

        img = image_cache.image(pk)
        if img is None:
            return Response(data={'error': 'Image #{} - not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)

        return Response(data={'status': 'Image #{} - cached'.format(pk)}, status=status.HTTP_200_OK)

    @action(['get'], detail=True, url_path='downsample')
    def downsample(self, request, pk=None):
        global image_cache

        image = image_cache.image(pk)
        if image is None:
            return Response(data={'error': 'Image #{} - not found'.format(pk)}, status=status.HTTP_404_NOT_FOUND)

        source_x = self._parse_int_param(request.query_params.get('source_x'), default=0, min_value=0)
        source_y = self._parse_int_param(request.query_params.get('source_y'), default=0, min_value=0)
        source_width = self._parse_int_param(request.query_params.get('source_width'), default=0, min_value=0)
        source_height = self._parse_int_param(request.query_params.get('source_height'), default=0, min_value=0)
        downscale = self._parse_float_param(request.query_params.get('downscale'), default=1, min_value=0.0001)
        quality = self._parse_int_param(request.query_params.get('quality'), default=95, min_value=1)

        width, height = image.width, image.height

        x = min(width, source_x)
        y = min(height, source_y)
        w = min(width - source_x, source_width)
        h = min(height - source_y, source_height)

        # TODO: check it
        # See: https://github.com/libvips/pyvips/issues/166
        image = image.crop(x, y, w, h)
        image = image.resize(downscale)
        data = image.write_to_buffer('.jpg', Q=quality)
        response = HttpResponse(data)

        response["Content-Type"] = 'image/jpeg'
        return response
