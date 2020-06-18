# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals
from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix.utils.statutils import do_rest_stat_action, using_stats_db
from django_szuprefix_saas.saas.mixins import PartyMixin
from rest_framework.response import Response

__author__ = 'denishuang'
from . import models, serializers,stats, helper
from rest_framework import viewsets, decorators
from django_szuprefix.api.decorators import register


@register()
class DailyLogViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.DailyLog.objects.all()
    serializer_class = serializers.DailyLogSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
    }

    @decorators.list_route(['POST'])
    def write(self, request):
        user = request.user
        for k, v in request.data.iteritems():
            log, created = self.party.dailylog_dailylogs.get_or_create(user=user, the_date=k)
            log.context.update(v)
            log.save()
        return Response({'detail': 'success'})


@register()
class StatViewSet(PartyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Stat.objects.all())
    serializer_class = serializers.StatSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull']
    }

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_stat)

@register()
class RecordViewSet(PartyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Record.objects.all())
    serializer_class = serializers.RecordSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull'],
        'owner_type': ['exact',],
        'user': ['exact',],
        'user_group': ['exact',],
        'owner_group': ['exact',]
    }

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_record)

@register()
class PerformanceViewSet(PartyMixin, viewsets.ModelViewSet):
    queryset = models.Performance.objects.all()
    serializer_class = serializers.PerformanceSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'update_time': ['exact', 'gte', 'lte', 'range'],
        'owner_id': ['exact', 'isnull', 'in'],
        'owner_type': ['exact',],
        'user': ['exact',],
        'user_group': ['exact',],
        'owner_group': ['exact',]
    }
    search_fields = ['owner_name', 'user_name', 'user_group', 'owner_group']

    @decorators.list_route(['GET'])
    def read(self, request):
        p = helper.get_performance(request.query_params, request.user, self.party)
        return Response(serializers.PerformanceSerializer(instance=p).data)

    @decorators.list_route(['POST'])
    def write(self, request):
        p = helper.save_performance(request.data, request.user, self.party)
        return Response(serializers.PerformanceSerializer(instance=p).data)
