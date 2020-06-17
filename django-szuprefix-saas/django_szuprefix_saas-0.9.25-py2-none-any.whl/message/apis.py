# -*- coding:utf-8 -*-
from django_szuprefix.api.mixins import BatchActionMixin

__author__ = 'denishuang'
from . import models, serializers
from rest_framework import viewsets, decorators, response
from django_szuprefix.api.decorators import register


@register()
class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer


@register()
class MessageViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    filter_fields = {
        "is_force": ['exact'],
        "is_read": ['exact'],
    }
    search_fields = ['title']

    @decorators.list_route(['POST'])
    def batch_read(self, request):
        from datetime import datetime
        return self.do_batch_action('is_read', True, extra_params={'read_time': datetime.now()})

    @decorators.detail_route(['POST'])
    def read(self, request, pk):
        from datetime import datetime
        message = self.get_object()
        message.is_read = True
        message.read_time = datetime.now()
        message.save()
        return response.Response({'detail': 'Success'})


