# -*- coding:utf-8 -*-
from django_szuprefix.api.mixins import BatchActionMixin
from rest_framework.serializers import Serializer

from . import models, mixins, serializers, permissions, signals

from rest_framework import viewsets, decorators, response
from django_szuprefix.api.decorators import register
from django_szuprefix.api.permissions import DjangoModelPermissionsWithView

__author__ = 'denishuang'


@register()
class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Party.objects.all()
    serializer_class = serializers.PartySerializer

    @decorators.list_route(['GET'], permission_classes=[])
    def current(self, request):
        host = request.META['SERVER_NAME']
        if '1.0.0.127' in host:
            party = self.queryset.filter(is_active=True).first()
        else:
            party = self.queryset.get(is_active=True, slug=host.split('.')[0])
        srs = signals.to_get_party_settings.send(sender=self, party=party, request=request)
        data = self.get_serializer(party).data
        ds = data['settings'] = {}
        for func, rs in srs:
            ds.update(rs)
        return response.Response(data)

@register()
class WorkerViewSet(mixins.PartyMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Worker.objects.all()
    serializer_class = serializers.WorkerSerializer
    permission_classes = [DjangoModelPermissionsWithView]
    filter_fields = {
        'number': ['exact', 'in']
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WorkerListSerializer
        return super(WorkerViewSet, self).get_serializer_class()

    @decorators.list_route(['get'], permission_classes=[permissions.IsSaasWorker])
    def current(self, request):
        serializer = serializers.CurrentWorkerSerializer(self.worker, context={'request': request})
        return response.Response(serializer.data)


    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)

