from rest_framework.generics import RetrieveAPIView
from djangopost.models import ArticleModel
from djangopost.rest_api.serializers import ArticleSerializer


class ArticleRetrieveViewset(RetrieveAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'