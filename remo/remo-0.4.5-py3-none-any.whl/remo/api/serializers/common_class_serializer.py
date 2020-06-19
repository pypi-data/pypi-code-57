from rest_framework import serializers

from remo_app.remo.models import Class


class CommonClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name')


class CommonClassNestedSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Class
        fields = ('id', 'name')
