# -*- coding:utf-8 -*-
from __future__ import division
from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix_saas.saas.mixins import PartyMixin
from rest_framework.viewsets import GenericViewSet

from . import models, serializers
from rest_framework import mixins, decorators
from django_szuprefix.api.decorators import register


@register()
class TodoViewSet(PartyMixin, UserApiMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer
    filter_fields = {
        'user': ['exact'],
        'is_done': ['exact'],
        'expiration': ['gt', 'lt']
    }

    def get_queryset(self):
        qset = super(TodoViewSet, self).get_queryset()
        if self.action == 'current':
            from datetime import datetime
            qset = qset.filter(user=self.request.user, is_done=False, expiration__gt=datetime.now())
        return qset

    @decorators.list_route(methods=['GET'])
    def current(self, request):
        return self.list(request)
