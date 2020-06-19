# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from ..api.mixins import UserApiMixin
from . import serializers, models
from rest_framework import viewsets, decorators
from ..api.decorators import register

__author__ = 'denishuang'

# @register()
# class ExcelViewSet(viewsets.ViewSet):
#     @decorators.list_route(['post'], authentication_classes=[], permission_classes=[])
#     def read(self, request, *args, **kwargs):
#         file_obj = request.FILES.get('file', None)
#         orient = request.data.get('orient', '')
#         if orient == 'blocks':
#             return Response(excelutils.pandas_read(file_obj, trim_null_rate=request.data.get('trim_null_rate', 0.5)))
#         else:
#             return Response({'data': excelutils.excel2json(file_obj)})
#
#     @decorators.list_route(['post'], authentication_classes=[], permission_classes=[])
#     def write(self, request, *args, **kwargs):
#         body = request.data
#         data = body.get("data")
#         file_name = body.get("file_name", "export_data.xlsx")
#         from excel_response import ExcelResponse
#         return ExcelResponse(data, output_filename=file_name)


@register()
class ImageViewSet(UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    user_field_name = 'owner'
    filter_fields = {
        'content_type__app_label': ['exact'],
        'content_type__model': ['exact']
    }


@register()
class TempFileViewSet(UserApiMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TempFileSerializer
    queryset = models.TempFile.objects.all()
    user_field_name = 'owner'



from django.contrib.contenttypes import models as ctmodels

@register()
class ContenttypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ctmodels.ContentType.objects.all().order_by('app_label')
    serializer_class = serializers.ContenttypeSerializer
    permission_classes = []
    search_fields = ('app_label', 'model')
    filter_fields = {
        'id': ['exact', 'in']
    }

    def filter_queryset(self, queryset):
        if self.action == 'all':
            return self.queryset
        from ..auth.helper import get_user_model_permissions
        from django.db.models import Q
        user = self.request.user
        qset = super(ContenttypeViewSet, self).filter_queryset(queryset)
        mps = get_user_model_permissions(user)
        ms = [m.split('.') for m in mps.keys()]
        lookup = None
        for m in ms:
            q = Q(**dict(app_label=m[0], model=m[1]))
            lookup = (lookup | q) if lookup else q
        return qset.filter(lookup) if lookup else qset

    @decorators.list_route(['GET'])
    def all(self, request):
        return self.list(request)