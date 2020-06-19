from rest_framework import serializers

from remo_app.remo.models import DatasetImage


class DatasetImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='original_name')
    url = serializers.SerializerMethodField()
    path = serializers.CharField(source='image_object.local_image')
    size = serializers.IntegerField(source='image_object.size')
    width = serializers.IntegerField(source='image_object.width')
    height = serializers.IntegerField(source='image_object.height')
    upload_date = serializers.DateTimeField(source='created_at')

    class Meta:
        model = DatasetImage
        fields = ('id', 'name', 'dataset_id', 'url', 'path', 'size', 'width', 'height', 'upload_date')

    def get_url(self, instance):
        return instance.image_url()
