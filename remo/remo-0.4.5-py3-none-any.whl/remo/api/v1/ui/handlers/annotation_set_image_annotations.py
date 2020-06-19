from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from remo_app.remo.api.viewsets import BaseGrandNestedModelViewSet
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.models import DatasetImage, AnnotationTags, Annotation, AnnotationSet, NewAnnotation


class AnnotationSetImageAnnotations(BaseGrandNestedModelViewSet):
    grand_parent_lookup = 'annotation_sets'
    parent_lookup = 'images'

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
            return (
                None,
                Response({'error': f'DatasetImage #{id} was not found.',}, status=status.HTTP_404_NOT_FOUND),
            )

        return image, None

    def _validate_annotation_set(self, **kwargs):
        id = kwargs.get('annotation_sets_pk')
        annotation_set = AnnotationSet.objects.filter(id=id).first()
        if not annotation_set:
            return (
                None,
                Response({'error': f'AnnotationSet #{id} was not found.',}, status=status.HTTP_404_NOT_FOUND),
            )

        return annotation_set, None

    def _get_annotation(self, image, annotation_set):
        annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
        if not annotation:
            annotation = Annotation.objects.create(image=image, annotation_set=annotation_set)
        return annotation

    def list(self, request, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, request, *args, **kwargs):
        image, resp = self._validate_image(**kwargs)
        if resp:
            return resp

        annotation_set, resp = self._validate_annotation_set(**kwargs)
        if resp:
            return resp

        annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
        if not annotation:
            return Response({'error': f'Annotation was not found.'}, status=status.HTTP_404_NOT_FOUND)

        annotation.delete_objects()
        new_annotation = NewAnnotation.objects.filter(image=annotation.image, annotation_set=annotation.annotation_set).first()
        if new_annotation:
            new_annotation.delete_objects()


        update_annotation_set_statistics(annotation_set)
        return Response(status=status.HTTP_204_NO_CONTENT)

