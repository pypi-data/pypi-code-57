from rest_framework.generics import RetrieveUpdateAPIView
from djangoarticle.models import CategoryModelScheme
from djangoarticle.rest_api.serializers import CategorySchemeSerializer
from djangoarticle.rest_api.permissions import IsOwnerOrReadOnly


class CategoryUpdateViewset(RetrieveUpdateAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]