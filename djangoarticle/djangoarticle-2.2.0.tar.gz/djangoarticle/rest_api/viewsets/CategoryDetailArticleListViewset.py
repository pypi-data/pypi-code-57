from rest_framework.generics import ListAPIView
from djangoarticle.models import ArticleModelScheme
from djangoarticle.rest_api.serializers import ArticleSchemeSerializer


class CategoryDetailArticleListViewset(ListAPIView):
    serializer_class = ArticleSchemeSerializer
    def get_queryset(self):
        return ArticleModelScheme.objects.published().filter(category__slug=self.kwargs['slug'])