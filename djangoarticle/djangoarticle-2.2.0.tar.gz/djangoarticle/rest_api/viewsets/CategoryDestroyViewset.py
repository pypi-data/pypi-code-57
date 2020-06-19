from rest_framework.generics import DestroyAPIView
from djangoarticle.models import CategoryModelScheme
from djangoarticle.rest_api.serializers import CategorySchemeSerializer
from djangoarticle.rest_api.permissions import IsOwnerOrReadOnly


class CategoryDestroyViewset(DestroyAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]