from rest_framework.generics import CreateAPIView
from djangopost.models import ArticleModel
from djangopost.rest_api.serializers import ArticleSerializer


class ArticleCreateViewset(CreateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer