# from django.contrib.postgres.aggregates import ArrayAgg as OrigArrayAgg
# from django.contrib.postgres.fields import ArrayField
# from django.db.models import Q
# from django_filters import filters
# from django_filters.rest_framework import DjangoFilterBackend, FilterSet
# from rest_framework import viewsets, mixins
# from rest_framework.filters import OrderingFilter
# import functools, operator
#
# from remo_app.remo.api.serializers import DatasetImageSerializer
# from remo_app.remo.models import DatasetImage
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
#     tags_not = CharInFilter(field_name='tag__name', exclude=True, distinct=True)
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
#                         'dataset__name__icontains',
#                         'original_name__icontains',
#                         'folder__name__icontains'
#                     )
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
#         return qs.annotate(tags_arr=ArrayAgg('tag__name')).filter(tags_arr__contains=value)
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
#                         'dataset__name__icontains',
#                         'original_name__icontains',
#                         'folder__name__icontains'
#                     )
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
#
#
# class DatasetImageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = DatasetImage.objects.all()
#     serializer_class = DatasetImageSerializer
#     filter_backends = (DjangoFilterBackend, OrderingFilter)
#     filter_class = DatasetImageFilterSet
#     ordering = 'id'
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(dataset__user=self.request.user)
