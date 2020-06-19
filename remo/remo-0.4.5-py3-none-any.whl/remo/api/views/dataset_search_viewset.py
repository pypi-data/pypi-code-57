# from django.contrib.postgres.aggregates import ArrayAgg as OrigArrayAgg
# from django.contrib.postgres.fields import ArrayField
# from django.db.models import Q
# from django_filters import filters
# from django_filters.rest_framework import DjangoFilterBackend, FilterSet
# from rest_framework import viewsets, mixins
# import itertools
#
# from remo_app.remo.models import Dataset, ImageFolder
# from remo_app.remo.api.utils import SliceableGenerator
# from remo_app.remo.api.serializers import DatasetSearchSerializer
#
#
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
# class FolderFilterSet(FilterSet):
#     name = CharInFilter()
#     is_archived = filters.BooleanFilter(field_name='dataset__is_archived')
#
#     classes = CharInFilter(method='classes_filter')
#     tags = CharInFilter(method='tags_filter')
#     tasks = CharInFilter(method='tasks_filter')
#     users = CharInFilter(method='users_filter')
#
#     # '_not' versions of above ones
#     classes_not = CharInFilter(method='classes_not_filter')
#     tags_not = CharInFilter(field_name='contents__tag__name', exclude=True, distinct=True)
#     tasks_not = CharInFilter(
#         field_name='dataset__annotation_sets__task__name',
#         exclude=True,
#         distinct=True
#     )
#     users_not = CharInFilter(field_name='dataset__user__username', exclude=True, distinct=True)
#
#     class Meta:
#         model = ImageFolder
#         fields = (
#             'classes', 'tags', 'tasks', 'users',
#             'classes_not', 'tags_not', 'tasks_not', 'users_not',
#             'name', 'is_archived'
#         )
#
#     def classes_filter(self, qs, name, value):
#         return qs.annotate(
#             classes1_arr=ArrayAgg('contents__annotations__classes__name'),
#             classes2_arr=ArrayAgg('contents__annotations__annotation_objects__classes__name')
#         ).filter(
#             Q(classes1_arr__contains=value) | Q(classes2_arr__contains=value)
#         )
#
#     def tags_filter(self, qs, name, value):
#         return qs.annotate(
#             tags_arr=ArrayAgg('contents__tag__name')
#         ).filter(
#             tags_arr__contains=value
#         )
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
#     def classes_not_filter(self, qs, name, value):
#         return qs.exclude(
#             Q(  # Image classification
#                 contents__annotations__classes__name__in=value
#             ) | Q(  # Object detection/object segmentation
#                 contents__annotations__annotation_objects__classes__name__in=value
#             )
#         ).distinct()
#
#
# class DatasetFilterSet(FilterSet):
#     name = CharInFilter()
#     is_archived = filters.BooleanFilter()
#
#     classes = CharInFilter(method='classes_filter')
#     tags = CharInFilter(method='tags_filter')
#     tasks = CharInFilter(method='tasks_filter')
#     users = CharInFilter(method='users_filter')
#
#     # '_not' versions of above ones
#     classes_not = CharInFilter(method='classes_not_filter')
#     tags_not = CharInFilter(field_name='dataset_images__tag__name', exclude=True, distinct=True)
#     tasks_not = CharInFilter(field_name='annotation_sets__task__name', exclude=True, distinct=True)
#     users_not = CharInFilter(field_name='user__username', exclude=True, distinct=True)
#
#     class Meta:
#         model = Dataset
#         fields = (
#             'classes', 'tags', 'tasks', 'users',
#             'classes_not', 'tags_not', 'tasks_not', 'users_not',
#             'name', 'is_archived'
#         )
#
#     def classes_filter(self, qs, name, value):
#         return qs.annotate(
#             classes1_arr=ArrayAgg('dataset_images__annotations__classes__name'),
#             classes2_arr=ArrayAgg('dataset_images__annotations__annotation_objects__classes__name')
#         ).filter(
#             Q(classes1_arr__contains=value) | Q(classes2_arr__contains=value)
#         )
#
#     def tags_filter(self, qs, name, value):
#         return qs.annotate(
#             tags_arr=ArrayAgg('dataset_images__tag__name')
#         ).filter(
#             tags_arr__contains=value
#         )
#
#     def tasks_filter(self, qs, name, value):
#         return qs.annotate(
#             tasks_arr=ArrayAgg('annotation_sets__task__name')
#         ).filter(
#             tasks_arr__contains=value
#         )
#
#     def users_filter(self, qs, name, value):
#         return qs.annotate(
#             users_arr=ArrayAgg('user__username')
#         ).filter(
#             users_arr__contains=value
#         )
#
#     def classes_not_filter(self, qs, name, value):
#         return qs.exclude(
#             Q(  # Image classification
#                 dataset_images__annotations__classes__name__in=value
#             ) | Q(  # Object detection/object segmentation
#                 dataset_images__annotations__annotation_objects__classes__name__in=value
#             )
#         ).distinct()
#
#
# class DatasetSearchViewSet(mixins.ListModelMixin,
#                            viewsets.GenericViewSet):
#     serializer_class = DatasetSearchSerializer
#     ordering_fields = ('name', 'created_at')
#
#     def get_queryset(self):
#         # TODO: restrict to team when it will be implemented, #272
#         record_type = self.request.query_params.get('record_type')
#         qs = {
#             'folder': ImageFolder.objects.filter(
#                 Q(dataset__user=self.request.user) | Q(dataset__is_public=True)
#             ).order_by('id'),
#             'dataset': Dataset.objects.filter(
#                 Q(user=self.request.user) | Q(is_public=True)
#             ).order_by('id')
#         }
#
#         # Apply filters
#         qs['folder'] = FolderFilterSet(
#             self.request.query_params,
#             queryset=qs['folder'],
#             request=self.request
#         ).qs
#         qs['dataset'] = DatasetFilterSet(
#             self.request.query_params,
#             queryset=qs['dataset'],
#             request=self.request
#         ).qs
#
#         # Apply ordering and filter out by record_type
#         qs = {
#             name: self.order_qs(q, self.request.query_params.get('ordering'))
#             for name, q in qs.items()
#             if name != record_type
#         }
#
#         return SliceableGenerator(
#             itertools.chain.from_iterable(qs.values()),
#             size=sum(q.count() for q in qs.values())
#         )
#
#     def order_qs(self, qs, param):
#         """
#         Apply ordering to a given queryset
#         :param qs:
#         :param param: 'ordering' parameter value
#         :return:
#         """
#         if not isinstance(param, str):
#             return qs
#
#         desc = param.startswith('-')
#         field = param[1:] if desc else param
#         if field not in self.ordering_fields:
#             return qs
#
#         return qs.order_by(param)
