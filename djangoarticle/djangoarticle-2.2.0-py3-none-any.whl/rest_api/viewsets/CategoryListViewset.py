from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from djangoarticle.models import CategoryModelScheme
from djangoarticle.rest_api.serializers import CategorySchemeSerializer


class CategoryListViewset(ListAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial',)