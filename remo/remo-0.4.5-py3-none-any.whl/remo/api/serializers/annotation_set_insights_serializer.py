from rest_framework import serializers


class AnnotationSetInsightSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_annotation_objects = serializers.IntegerField()
    total_images = serializers.IntegerField()
    objects_per_image = serializers.FloatField()


class AnnotationSetInsightsSerializer(serializers.Serializer):
    record_type = serializers.CharField()
    class_ = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    @property
    def fields(self):
        fields = super().fields
        fields['class'] = fields.pop('class_')

        return fields

    def get_class_(self, instance):
        if instance['record_type'] != 'class':
            return None

        return AnnotationSetInsightSerializer(instance, context=self.context).data

    def get_tag(self, instance):
        if instance['record_type'] != 'tag':
            return None

        return AnnotationSetInsightSerializer(instance, context=self.context).data
