from rest_framework.generics import ListAPIView
from djangopost.models import ArticleModel
from djangopost.rest_api.serializers import ArticleSerializer


class TaggitDetailArticleListViewset(ListAPIView):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        return ArticleModel.objects.published().filter(tags__slug=self.kwargs['slug'])