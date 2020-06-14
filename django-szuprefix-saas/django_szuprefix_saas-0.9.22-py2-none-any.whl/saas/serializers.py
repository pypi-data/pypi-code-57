# -*- coding:utf-8 -*-
from rest_framework.validators import UniqueTogetherValidator

__author__ = 'denishuang'
from . import models, mixins
from rest_framework import serializers


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Party
        fields = ('name', 'logo')


class WorkerSerializer(mixins.PartySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Worker
        fields = ('name', 'number', 'profile', 'position')
        validators = [UniqueTogetherValidator(
            queryset=model.objects.all(),
            fields=['party', 'number'],
            message="相同的编号已存在"
        )]

class WorkerListSerializer(WorkerSerializer):
    class Meta(WorkerSerializer.Meta):
        fields = ('id', 'name', 'number', 'position', 'is_active')


class CurrentWorkerSerializer(WorkerSerializer):
    party = serializers.StringRelatedField()

    class Meta(WorkerSerializer.Meta):
        fields = ('name', 'number', 'position', 'party', 'departments')
