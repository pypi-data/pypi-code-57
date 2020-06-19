from rest_framework.generics import DestroyAPIView
from djangoarticle.models import ArticleModelScheme
from djangoarticle.rest_api.serializers import ArticleSchemeSerializer
from djangoarticle.rest_api.permissions import IsOwnerOrReadOnly


class ArticleDestroyViewset(DestroyAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]