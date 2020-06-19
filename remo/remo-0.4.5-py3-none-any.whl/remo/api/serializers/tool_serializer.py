from rest_framework import serializers

from remo_app.remo.models import Tool


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'
