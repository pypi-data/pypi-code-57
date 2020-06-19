from rest_framework import serializers

from remo_app.remo.api.serializers import ToolSerializer
from remo_app.remo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    available_tools = ToolSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'
