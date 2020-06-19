from django.db.models import Q
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import serializers

from remo_app.remo.models import AnnotationSet
from remo_app.remo.api.viewsets import BaseNestedModelViewSet


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


class AnnotationSetInsights(mixins.ListModelMixin,
                            BaseNestedModelViewSet):
    parent_lookup = 'annotation_sets'

    def get_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def list(self, request, *args, **kwargs):
        annotation_set = self.get_parent_object_or_404()

        total_images = annotation_set.dataset.quantity

        stat = annotation_set.statistics.first()
        data = []
        if not stat:
            return Response({
                'total_annotated_images': total_images,
                'total_annotation_objects': 0,
                'results': data
            })

        for class_name, class_stat in stat.classes.items():
            n_objs = class_stat.get('n_objs', 0)
            n_imgs = class_stat.get('n_imgs', 0)
            if n_imgs > 0 and n_objs > 0:
                objs_per_img = n_objs / n_imgs
            else:
                objs_per_img = 'N/A'
            data.append({
                'record_type': 'class',
                'class': {
                    'name': class_name,
                    'objects_per_image': objs_per_img,
                    'total_annotation_objects': n_objs,
                    'total_images': n_imgs,
                }
            })

        if stat.tags:
            for tag_name, count in stat.tags:
                data.append({
                    'record_type': 'tag',
                    'tag': {
                        'name': tag_name,
                        'total_images': count,
                        'total_annotation_objects': 0,
                    }
                })

        results = {
            'total_annotated_images': total_images,
            'total_annotation_objects': stat.total_annotation_objects,
            'results': data
        }
        return Response(results)
