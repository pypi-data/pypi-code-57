from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.use_cases.classes import capitalize_class_name
from remo_app.remo.use_cases.delete_class import delete_class_in_annotation_set
from remo_app.remo.use_cases.rename_class import rename_class_in_annotation_set
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.models import AnnotationSet, Class


class AnnotationSetClasses(BaseNestedModelViewSet):
    parent_lookup = 'annotation_sets'

    def get_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def _validate_annotation_set(self, **kwargs):
        annotation_set_id = kwargs.get('annotation_sets_pk')
        annotation_set = self.get_parent_queryset().filter(id=annotation_set_id).first()
        if not annotation_set:
            return None, Response({
                'error': 'Annotation set #{} was not found'.format(annotation_set_id),
            }, status=status.HTTP_404_NOT_FOUND)

        if self.request.user != annotation_set.dataset.user:
            # TODO: check later in dataset.users_shared
            return annotation_set, Response({
                'error': 'Only dataset owner can add new classes to annotation set.',
            }, status=status.HTTP_403_FORBIDDEN)

        return annotation_set, None

    def _validate_new_class_name(self, request):
        name = request.data.get('name', '')
        if not name:
            return None, Response({
                'error': 'Class name should not be empty',
            }, status=status.HTTP_400_BAD_REQUEST)

        name = capitalize_class_name(name)
        return name, None

    def _validate_create_inputs(self, request, **kwargs):
        annotation_set, resp = self._validate_annotation_set(**kwargs)
        if resp:
            return None, None, resp

        name, resp = self._validate_new_class_name(request)
        if resp:
            return None, None, resp

        return annotation_set, name, None

    def create(self, request, *args, **kwargs):
        annotation_set, name, resp = self._validate_create_inputs(request, **kwargs)
        if resp:
            return resp

        obj, _ = Class.objects.get_or_create(name=name)

        resp_status = status.HTTP_200_OK
        annotation_set_classes = {class_obj.id for class_obj in annotation_set.classes.distinct()}
        if obj.id not in annotation_set_classes:
            annotation_set.classes.add(obj.id)
            annotation_set.save()

            resp_status = status.HTTP_201_CREATED
            update_annotation_set_statistics(annotation_set)

        return Response({
            'id': obj.id,
            'name': name,
        }, status=resp_status)

    def _validate_class_id(self, **kwargs):
        class_id = kwargs.get('pk')
        try:
            class_id = int(class_id)
        except ValueError:
            return None, Response({
                'error': f"Class id - {class_id}, not a valid id",
            }, status=status.HTTP_400_BAD_REQUEST)
        return class_id, None

    def _validate_update_inputs(self, request, **kwargs):
        annotation_set, name, resp = self._validate_create_inputs(request, **kwargs)
        if resp:
            return None, None, None, resp

        class_id, resp = self._validate_class_id(**kwargs)
        if resp:
            return None, None, None, resp

        annotation_set_classes = {class_obj.id for class_obj in annotation_set.classes.distinct()}
        if class_id not in annotation_set_classes:
            return None, None, None, Response({
                'error': f"Class id: {class_id}, not found in annotation set: '{annotation_set.name}'",
            }, status=status.HTTP_404_NOT_FOUND)

        return annotation_set, name, class_id, None

    def update(self, request, *args, **kwargs):
        annotation_set, name, class_id, resp = self._validate_update_inputs(request, **kwargs)
        if resp:
            return resp

        obj, _ = Class.objects.get_or_create(name=name)
        if obj.id != class_id:
            rename_class_in_annotation_set(annotation_set.id, class_id, obj.id)

        return Response({
            'id': obj.id,
            'name': name,
        }, status=status.HTTP_200_OK)

    def _validate_destroy_inputs(self, request, **kwargs):
        annotation_set, resp = self._validate_annotation_set(**kwargs)
        if resp:
            return None, None, resp

        class_id, resp = self._validate_class_id(**kwargs)
        if resp:
            return None, None, resp

        annotation_set_classes = {class_obj.id for class_obj in annotation_set.classes.distinct()}
        if class_id not in annotation_set_classes:
            return None, None, None, Response({
                'error': f"Class id: {class_id}, not found in annotation set: '{annotation_set.name}'",
            }, status=status.HTTP_404_NOT_FOUND)

        return annotation_set, class_id, None

    def destroy(self, request, *args, **kwargs):
        annotation_set, class_id, resp = self._validate_destroy_inputs(request, **kwargs)
        if resp:
            return resp

        delete_class_in_annotation_set(annotation_set.id, class_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
