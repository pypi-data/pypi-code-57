from rest_framework import filters, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from huscy.subjects import pagination, models, serializers, services
from huscy.subjects.permissions import ChangeSubjectPermission, DjangoModelPermissionsWithViewCheck


class ContactViewSet(viewsets.ModelViewSet):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = (DjangoModelPermissionsWithViewCheck, )


class PhoneViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Phone.objects.all()
    serializer_class = serializers.PhoneSerializer
    permission_classes = (DjangoModelPermissions, )


class AddressViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (DjangoModelPermissions, )


class SubjectViewSet(viewsets.ModelViewSet):
    filter_backends = (
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = (
        'contact__date_of_birth',
        'contact__first_name',
        'contact__gender',
        'contact__last_name',
    )
    pagination_class = pagination.SubjectPagination
    permission_classes = (DjangoModelPermissionsWithViewCheck, )
    queryset = (models.Subject.objects.prefetch_related('contact', 'guardians')
                                      .order_by('contact__last_name', 'contact__first_name'))
    search_fields = 'contact__display_name', 'contact__date_of_birth'
    serializer_class = serializers.SubjectSerializer

    def list(self, request):
        '''
        For data protection reasons it's necessary to limit the number of returned subjects to 500.
        Unfortunately it is not possible to limit the queryset because filters cannot be applied
        to a sliced queryset. For this reason, the limiting have to be done after filtering.
        '''
        filtered_queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset = self.paginate_queryset(filtered_queryset[:500])
        serializer = self.get_serializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('delete', 'post'), permission_classes=(ChangeSubjectPermission, ))
    def inactivity(self, request, pk):
        if request.method == 'DELETE':
            return self._delete_inactivity()
        elif request.method == 'POST':
            return self._create_inactivity(request)

    def _delete_inactivity(self):
        services.unset_inactivity(self.get_object())
        return Response(status=HTTP_204_NO_CONTENT)

    def _create_inactivity(self, request):
        serializer = serializers.InactivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
