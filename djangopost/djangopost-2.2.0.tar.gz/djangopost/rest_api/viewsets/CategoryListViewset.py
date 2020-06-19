from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from djangopost.models import CategoryModel
from djangopost.rest_api.serializers import CategorySerializer


class CategoryListViewset(ListAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial',)