from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from djangoarticle.models import ArticleModelScheme
from djangoarticle.rest_api.serializers import ArticleSchemeSerializer


class ArticleListPromoViewset(ListAPIView):
    queryset = ArticleModelScheme.objects.promotional()
    serializer_class = ArticleSchemeSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial',)