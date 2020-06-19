from rest_framework.generics import RetrieveUpdateAPIView
from djangopost.models import ArticleModel
from djangopost.rest_api.serializers import ArticleSerializer
from djangopost.rest_api.permissions import IsOwnerOrReadOnly


class ArticleUpdateViewset(RetrieveUpdateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]