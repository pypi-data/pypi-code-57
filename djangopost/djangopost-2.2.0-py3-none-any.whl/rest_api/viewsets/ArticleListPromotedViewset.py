from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from djangopost.models import ArticleModel
from djangopost.rest_api.serializers import ArticleSerializer


class ArticleListPromotedViewset(ListAPIView):
    queryset = ArticleModel.objects.promoted()
    serializer_class = ArticleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('serial',)