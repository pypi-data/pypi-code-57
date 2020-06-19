from rest_framework.generics import RetrieveAPIView
from djangoarticle.models import ArticleModelScheme
from djangoarticle.rest_api.serializers import ArticleSchemeSerializer


class ArticleRetrieveViewset(RetrieveAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    lookup_field = 'slug'