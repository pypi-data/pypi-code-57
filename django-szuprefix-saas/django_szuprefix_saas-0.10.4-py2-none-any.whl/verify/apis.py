# -*- coding:utf-8 -*-
from __future__ import division
from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix.utils.statutils import do_rest_stat_action
from django_szuprefix_saas.saas.mixins import PartyMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, stats, choices
from rest_framework import mixins, decorators
from django_szuprefix.api.decorators import register
from ..saas.helper import get_default_party


@register()
class VerifyViewSet(PartyMixin, UserApiMixin, ModelViewSet):
    queryset = models.Verify.objects.all()
    serializer_class = serializers.VerifySerializer
    filter_fields = {
        'category': ['exact'],
        'create_time': ['range'],
        'status': ['exact']
    }
    search_fields = ['name']

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_verify)

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)

    def get_permissions(self):
        if self.action in ['current']:
            self.party = get_default_party()
            return [IsAuthenticated()]
        return super(VerifyViewSet, self).get_permissions()

    def get_queryset(self):
        qset = super(VerifyViewSet, self).get_queryset()
        if self.action == 'current':
            qset = qset.filter(user=self.request.user, status=choices.STATUS_PENDING)
        return qset

    @decorators.list_route(methods=['GET'])
    def current(self, request):
        return self.list(request)
