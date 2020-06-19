from rest_framework import serializers

from remo_app.remo.models import AnnotationTags, Tag


class BriefTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='tag.id')
    name = serializers.CharField(source='tag.name', max_length=255)
    annotation_set = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AnnotationTags
        fields = ('id', 'name', 'annotation_set', 'image')


class AnnotationSetImageTagSerializer(TagSerializer):
    def create(self, validated_data):
        validated_data['image'] = self.context['dataset_image']
        validated_data['annotation_set'] = self.context['annotation_set']
        self.context['dataset_image'].dataset.update()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['image'] = self.context['dataset_image']
        validated_data['annotation_set'] = self.context['annotation_set']
        self.context['dataset_image'].dataset.update()
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'annotation_set', 'image')


class TagAutocompleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
