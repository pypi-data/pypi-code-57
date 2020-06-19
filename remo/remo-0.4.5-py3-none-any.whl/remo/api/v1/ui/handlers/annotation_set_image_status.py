from django.db.models import Q
from django.http import JsonResponse
from rest_framework import mixins, status
from rest_framework.response import Response

from remo_app.remo.api.constants import AnnotationStatus, default_status
from remo_app.remo.api.viewsets import BaseGrandNestedModelViewSet
from remo_app.remo.use_cases.annotation import update_new_annotation
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.models import DatasetImage, AnnotationTags, Annotation, AnnotationSet


class AnnotationSetImageStatus(mixins.ListModelMixin, BaseGrandNestedModelViewSet):
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

    def _get_or_create_annotation(self, image, annotation_set):
        annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
        if not annotation:
            annotation = Annotation.objects.create(image=image, annotation_set=annotation_set)
        return annotation

    def _validate_status(self, request):
        status = request.data.get('status', default_status.name)
        status = str(status).strip()
        if not status:
            return (
                None,
                Response({'error': 'Tag name should not be empty',}, status=status.HTTP_400_BAD_REQUEST),
            )

        try:
            status = AnnotationStatus.by_name(status)
        except ValueError:
            status = default_status

        return status, None

    def create(self, request, *args, **kwargs):
        image, resp = self._validate_image(**kwargs)
        if resp:
            return resp

        annotation_set, resp = self._validate_annotation_set(**kwargs)
        if resp:
            return resp

        status, resp = self._validate_status(request)
        if resp:
            return resp

        annotation = self._get_or_create_annotation(image, annotation_set)
        annotation.status = status
        annotation.save()

        update_new_annotation(annotation)
        update_annotation_set_statistics(annotation_set)

        return JsonResponse({'status': status.name})
