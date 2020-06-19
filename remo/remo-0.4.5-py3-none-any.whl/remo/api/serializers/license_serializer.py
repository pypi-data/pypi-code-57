from rest_framework import serializers
from remo_app.remo.models import License


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'
        read_only_fields = ('id', 'name', 'description')
