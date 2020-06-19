from django.db.models import QuerySet
from rest_framework.viewsets import GenericViewSet
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from remo_app.remo.api.permissions import ValidParentPkPermission, ValidGrandParentPkPermission


class BaseNestedModelViewSet(GenericViewSet):
    """
        ViewSet for cases when double nesting of objects needed.
        Example: Project -> Dataset
        url: /api/project/<project_id>/dataset/<dataset_id>/
        In this example project is parent
    """
    parent_lookup = 'parent'
    parent_pk = None
    parent_queryset = None
    permission_classes = (ValidParentPkPermission,)

    def get_parent_queryset(self):
        assert self.parent_queryset is not None, (
            "'%s' should either include a `parent_queryset` attribute, "
            "or override the `get_parent_queryset()` method."
            % self.__class__.__name__
        )

        parent_queryset = self.parent_queryset
        if isinstance(parent_queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            parent_queryset = parent_queryset.all()
        return parent_queryset

    def is_valid_parent_pk(self):
        parent_queryset = self.get_parent_queryset()
        if self.parent_pk is not None and parent_queryset.filter(id=self.parent_pk).exists():
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        # get parent_pk from url arguments
        try:
            self.parent_pk = int(kwargs.get('%s_pk' % self.parent_lookup, 0))
        except (ValueError, TypeError):
            self.parent_pk = None
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['parent_pk'] = self.parent_pk
        return ctx

    def get_parent_object_or_404(self):
        """Shortcut method, tries to get parent record or raises 404"""
        try:
            record = self.get_parent_queryset().get(pk=self.parent_pk)
        except ObjectDoesNotExist:
            raise Http404
        return record


class BaseGrandNestedModelViewSet(BaseNestedModelViewSet):
    """
        ViewSet for cases when triple nesting of objects needed.
        Example: Project -> Dataset -> Image
        url: /api/project/<project_id>/dataset/<dataset_id>/image/<image_id>/
        In this example project is grand parent and dataset is parent
    """
    grand_parent_lookup = 'grand_parent'
    grand_parent_pk = None
    grand_parent_queryset = None
    permission_classes = (ValidGrandParentPkPermission, ValidParentPkPermission)

    def get_grand_parent_queryset(self):
        assert self.grand_parent_queryset is not None, (
            "'%s' should either include a `grand_parent_queryset` attribute, "
            "or override the `get_grand_parent_queryset()` method."
            % self.__class__.__name__
        )

        get_parent_queryset = self.grand_parent_queryset
        if isinstance(get_parent_queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            get_parent_queryset = get_parent_queryset.all()
        return get_parent_queryset

    def dispatch(self, request, *args, **kwargs):
        # get grand_parent_pk from url arguments
        try:
            self.grand_parent_pk = int(kwargs.get('%s_pk' % self.grand_parent_lookup, 0))
        except (ValueError, TypeError):
            self.grand_parent_pk = None
        return super().dispatch(request, *args, **kwargs)

    def is_valid_grand_parent_pk(self):
        grand_parent_queryset = self.get_grand_parent_queryset()
        if self.grand_parent_pk is not None and grand_parent_queryset.filter(id=self.grand_parent_pk).exists():
            return True

        return False

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['grand_parent_pk'] = self.grand_parent_pk
        return ctx

    def get_grand_parent_object_or_404(self):
        """
        Shortcut method, tries to get grandparent record or raises 404
        """
        try:
            r = self.get_grand_parent_queryset()
            record = r.get(pk=self.grand_parent_pk)
        except ObjectDoesNotExist:
            raise Http404

        return record
