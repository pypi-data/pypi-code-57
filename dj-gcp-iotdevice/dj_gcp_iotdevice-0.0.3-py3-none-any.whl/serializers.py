"""
Simple serializer for the GCP IoT Device structure.
"""

from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    """Simple serializer that represents the shape of a GCP IoT Device.
    """
    id = serializers.CharField()
    public_key = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
