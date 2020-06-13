# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django_szuprefix.api.mixins import UserApiMixin
from django_szuprefix_saas.saas.mixins import PartyMixin
from django_szuprefix_saas.saas.permissions import IsSaasWorker

from . import serializers, models
from rest_framework import viewsets, decorators, response, exceptions
from django_szuprefix.api.decorators import register

__author__ = 'denishuang'


@register()
class CommentViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = [IsSaasWorker]
    filter_fields = {
        'content_type': ['exact'],
        'object_id': ['exact'],
        'user': ['exact'],
        'create_time': ['range'],
        'reply_count': ['gte', 'lte']
    }

    def filter_queryset(self, queryset):
        qset = super(CommentViewSet, self).filter_queryset(queryset)
        ct = self.request.query_params.get('content_type')
        if not ct and self.action == 'list':
            return qset.exclude(content_type=ContentType.objects.get_for_model(models.Comment))
        return qset


@register()
class FavoriteViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.FavoriteSerializer
    queryset = models.Favorite.objects.all()
    permission_classes = [IsSaasWorker]
    filter_fields = {
        'content_type': ['exact'],
        'object_id': ['exact'],
        'user': ['exact'],
        'create_time': ['range']
    }

    @decorators.list_route(['GET', 'POST'])
    def record(self, request):
        qs = request.query_params
        if not qs.get('content_type'):
            raise exceptions.ValidationError('content_type should not be empty.')
        if not qs.get('object_id'):
            raise exceptions.ValidationError('object_id should not be empty.')
        qd = dict(user=request.user, content_type=qs.get('content_type'), object_id=qs.get('object_id'))
        f = self.get_queryset().filter(**qd).first()
        if request.method == 'GET':
            if not f:
                return response.Response(qs)
        elif request.method == 'POST':
            if not f:
                qd['content_type'] = ContentType.objects.get(id=qd['content_type'])
                f = models.Favorite(party=self.party, **qd)
            d = request.data
            f.notes[d['anchor']] = d
            f.save()
        return response.Response(self.get_serializer_class()(f).data)


@register()
class RatingViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.RatingSerializer
    queryset = models.Rating.objects.all()
    permission_classes = [IsSaasWorker]
    filter_fields = {
        'content_type__app_label': ['exact'],
        'content_type__model': ['exact'],
        'content_type': ['exact'],
        'object_id': ['exact'],
        'user': ['exact']
    }

    def submit(self):
        pass
