# -*- coding:utf-8 -*-
from __future__ import division
from django_szuprefix.api.mixins import UserApiMixin, BatchActionMixin
from django_szuprefix_saas.saas.mixins import PartyMixin
from . import models, serializers
from rest_framework import viewsets, decorators, response
from django_szuprefix.api.decorators import register


@register()
class SurveyViewSet(PartyMixin, UserApiMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Survey.objects.all()
    serializer_class = serializers.SurveySerializer
    search_fields = ('title',)
    filter_fields = {
        'id': ['in', 'exact'],
        'is_active': ['exact'],
        'content': ['contains'],
        'begin_time': ['range']
    }
    ordering_fields = ('is_active', 'title', 'create_time', 'questions_count')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SurveyListSerializer
        return super(SurveyViewSet, self).get_serializer_class()

    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)

    @decorators.detail_route(['GET'])
    def result(self, request, pk):
        from . import helper
        survey = helper.stat_survey_answers(self.get_object())
        serializer = self.get_serializer_class()(survey)
        return response.Response(serializer.data)

@register()
class AnswerViewSet(PartyMixin, UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    filter_fields = ('survey', 'user')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AnswerListSerializer
        return super(AnswerViewSet, self).get_serializer_class()


