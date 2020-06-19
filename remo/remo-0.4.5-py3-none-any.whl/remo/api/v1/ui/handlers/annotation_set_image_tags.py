from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework import serializers

from remo_app.remo.api.viewsets import BaseGrandNestedModelViewSet
from remo_app.remo.use_cases.annotation import update_new_annotation
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import count_tags, \
    get_or_create_annotation_set_statistics
from remo_app.remo.models import DatasetImage, Tag, AnnotationTags, Annotation, AnnotationSet


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='tag.id')
    name = serializers.CharField(source='tag.name', max_length=255)
    annotation_set = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AnnotationTags
        fields = ('id', 'name', 'annotation_set', 'image')


class AnnotationSetImageTags(mixins.ListModelMixin,
                             BaseGrandNestedModelViewSet):
    grand_parent_lookup = 'annotation_sets'
    parent_lookup = 'images'
    serializer_class = TagSerializer

    def get_grand_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def get_parent_queryset(self):
        annotation_set = self.get_grand_parent_object_or_404()
        return DatasetImage.objects.filter(dataset=annotation_set.dataset)

    def get_queryset(self):
        dataset_image = self.get_parent_object_or_404()
        annotation_set = self.get_grand_parent_object_or_404()
        return AnnotationTags.objects.filter(image=dataset_image, annotation_set=annotation_set)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['dataset_image'] = self.get_parent_object_or_404()
        ctx['annotation_set'] = self.get_grand_parent_object_or_404()
        return ctx

    def _validate_image(self, **kwargs):
        id = kwargs.get('images_pk')
        image = DatasetImage.objects.filter(id=id).first()
        if not image:
            return None, Response({
                'error': f'DatasetImage #{id} was not found.',
            }, status=status.HTTP_404_NOT_FOUND)

        return image, None

    def _validate_annotation_set(self, **kwargs):
        id = kwargs.get('annotation_sets_pk')
        annotation_set = AnnotationSet.objects.filter(id=id).first()
        if not annotation_set:
            return None, Response({
                'error': f'AnnotationSet #{id} was not found.',
            }, status=status.HTTP_404_NOT_FOUND)

        return annotation_set, None

    def _get_or_create_annotation(self, image, annotation_set):
        annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
        if not annotation:
            annotation = Annotation.objects.create(
                image=image,
                annotation_set=annotation_set
            )
        return annotation

    def _validate_tag(self, request):
        name = request.data.get('name', '')
        name = name.strip().lower()
        if not name:
            return None, Response({
                'error': 'Tag name should not be empty',
            }, status=status.HTTP_400_BAD_REQUEST)

        tag, _ = Tag.objects.get_or_create(name=name)
        return tag, None

    def create(self, request, *args, **kwargs):
        image, resp = self._validate_image(**kwargs)
        if resp:
            return resp

        annotation_set, resp = self._validate_annotation_set(**kwargs)
        if resp:
            return resp

        tag, resp = self._validate_tag(request)
        if resp:
            return resp

        annotation = self._get_or_create_annotation(image, annotation_set)
        annotation_tag = AnnotationTags.objects.filter(tag=tag, image=image, annotation=annotation, annotation_set=annotation_set).first()
        if annotation_tag:
            resp_status = status.HTTP_200_OK
        else:
            annotation_tag = AnnotationTags(tag=tag, image=image, annotation=annotation, annotation_set=annotation_set)
            annotation_tag.save()
            self.update_annotation_set_tags_statistics(annotation_tag.annotation_set, annotation_tag.annotation)
            resp_status = status.HTTP_201_CREATED

        return Response({
            'id': tag.id,
            'name': tag.name,
            'annotation_set': annotation_set.id,
            'image': image.id
        }, status=resp_status)

    def destroy(self, request, *args, **kwargs):
        image = DatasetImage.objects.get(id=kwargs.get('images_pk'))
        annotation_set = AnnotationSet.objects.get(id=kwargs.get('annotation_sets_pk'))
        annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
        pk = kwargs.get('pk')

        annotation_tag = AnnotationTags.objects.filter(tag_id=pk, annotation=annotation).first()
        if annotation_tag:
            annotation_set = annotation_tag.annotation_set
            annotation_tag.delete()
            self.update_annotation_set_tags_statistics(annotation_set, annotation)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update_annotation_set_tags_statistics(annotation_set: AnnotationSet, annotation: Annotation):
        tags = count_tags(annotation_set.id)
        stat = get_or_create_annotation_set_statistics(annotation_set)
        stat.tags = tags
        stat.save()

        update_new_annotation(annotation)
