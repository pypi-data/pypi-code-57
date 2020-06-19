from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import AnnotationTags, AnnotationSet, Tag
from remo_app.remo.use_cases.delete_tag import delete_tag_in_annotation_set
from remo_app.remo.use_cases.rename_tag import rename_tag_in_annotation_set


class AnnotationSetTags(BaseNestedModelViewSet):
    parent_lookup = 'annotation_sets'

    def get_parent_queryset(self):
        return AnnotationSet.objects.filter(Q(user=self.request.user) | Q(dataset__is_public=True))

    def _validate_annotation_set(self, write_access=True, **kwargs):
        annotation_set_id = kwargs.get('annotation_sets_pk')
        annotation_set = self.get_parent_queryset().filter(id=annotation_set_id).first()
        if not annotation_set:
            return None, Response({
                'error': 'Annotation set #{} was not found'.format(annotation_set_id),
            }, status=status.HTTP_404_NOT_FOUND)

        if write_access and self.request.user != annotation_set.dataset.user:
            # TODO: check later in dataset.users_shared
            return annotation_set, Response({
                'error': 'Only dataset owner can edit annotation set.',
            }, status=status.HTTP_403_FORBIDDEN)

        return annotation_set, None

    def list(self, request, *args, **kwargs):
        annotation_set, resp = self._validate_annotation_set(write_access=False, **kwargs)
        if resp:
            return resp

        tt = AnnotationTags.objects.filter(annotation_set=annotation_set).values_list('tag__id', 'tag__name').distinct()
        tags = [{'id': id, 'name': name} for id, name in tt]

        return Response({
            'count': len(tags),
            'next': None,
            'previous': None,
            'results': tags
        })

    def _validate_tag_id(self, **kwargs):
        tag_id = kwargs.get('pk')
        try:
            tag_id = int(tag_id)
        except ValueError:
            return None, Response({
                'error': f"Tag id - {tag_id}, not a valid id",
            }, status=status.HTTP_400_BAD_REQUEST)
        return tag_id, None

    def _validate_new_tag_name(self, request):
        name = request.data.get('name', '')
        name = str(name).strip()
        if not name:
            return None, Response({
                'error': 'Tag name should not be empty',
            }, status=status.HTTP_400_BAD_REQUEST)

        return name, None

    def _validate_tag_in_annotation_set(self, annotation_set, tag_id):
        count = AnnotationTags.objects.filter(annotation_set=annotation_set, tag_id=tag_id).count()
        if count == 0:
            return Response({
                'error': f"Tag id: {tag_id}, not found in annotation set: '{annotation_set.name}'",
            }, status=status.HTTP_404_NOT_FOUND)

    def _validate_update_inputs(self, request, **kwargs):
        annotation_set, resp = self._validate_annotation_set(request, **kwargs)
        if resp:
            return None, None, None, resp

        tag_id, resp = self._validate_tag_id(**kwargs)
        if resp:
            return None, None, None, resp

        resp = self._validate_tag_in_annotation_set(annotation_set, tag_id)
        if resp:
            return None, None, None, resp

        name, resp = self._validate_new_tag_name(request)
        if resp:
            return None, None, None, resp

        return annotation_set, tag_id, name, None

    def update(self, request, *args, **kwargs):
        annotation_set, tag_id, name, resp = self._validate_update_inputs(request, **kwargs)
        if resp:
            return resp

        obj, _ = Tag.objects.get_or_create(name=name)
        if obj.id != tag_id:
            rename_tag_in_annotation_set(annotation_set.id, tag_id, obj.id)

        return Response({
            'id': obj.id,
            'name': name,
        }, status=status.HTTP_200_OK)

    def _validate_destroy_inputs(self, request, **kwargs):
        annotation_set, resp = self._validate_annotation_set(**kwargs)
        if resp:
            return None, None, resp

        tag_id, resp = self._validate_tag_id(**kwargs)
        if resp:
            return None, None, resp

        resp = self._validate_tag_in_annotation_set(annotation_set, tag_id)
        if resp:
            return None, None, resp

        return annotation_set, tag_id, None

    def destroy(self, request, *args, **kwargs):
        annotation_set, tag_id, resp = self._validate_destroy_inputs(request, **kwargs)
        if resp:
            return resp

        delete_tag_in_annotation_set(annotation_set.id, tag_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
