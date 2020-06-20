# -*- coding:utf-8 -*- 
__author__ = 'denishuang'
from django_filters.rest_framework import filters

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)

class EmptyCharFilter(filters.CharFilter):
    empty_value = 'EMPTY'

    def filter(self, qs, value):
        if value != self.empty_value:
            return super(EmptyCharFilter, self).filter(qs, value)

        qs = self.get_method(qs)(**{'%s__%s' % (self.field_name, self.lookup_expr): ""})
        return qs.distinct() if self.distinct else qs