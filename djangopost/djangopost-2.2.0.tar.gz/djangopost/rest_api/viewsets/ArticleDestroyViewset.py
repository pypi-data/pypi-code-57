from rest_framework.generics import DestroyAPIView
from djangopost.models import ArticleModel
from djangopost.rest_api.serializers import ArticleSerializer
from djangopost.rest_api.permissions import IsOwnerOrReadOnly


class ArticleDestroyViewset(DestroyAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]