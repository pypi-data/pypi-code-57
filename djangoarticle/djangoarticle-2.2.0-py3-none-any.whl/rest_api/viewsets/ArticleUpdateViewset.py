from rest_framework.generics import RetrieveUpdateAPIView
from djangoarticle.models import ArticleModelScheme
from djangoarticle.rest_api.serializers import ArticleSchemeSerializer
from djangoarticle.rest_api.permissions import IsOwnerOrReadOnly


class ArticleUpdateViewset(RetrieveUpdateAPIView):
    queryset = ArticleModelScheme.objects.all()
    serializer_class = ArticleSchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]