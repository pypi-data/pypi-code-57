from rest_framework import status
from rest_framework.response import Response


class UpdateDatasetModelMixin:
    """
        Update a dataset instance.
        Only admin users can update public datasets.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.is_public and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyDatasetModelMixin:
    """
        Destroy a dataset instance.
        Only admin users can destroy public datasets.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_public and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class DestroyImageModelMixin:
    """
            Destroy a image instance.
            Only admin users can destroy public images.
        """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.dataset.is_public and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
