from rest_framework.generics import DestroyAPIView
from djangopost.models import CategoryModel
from djangopost.rest_api.serializers import CategorySerializer
from djangopost.rest_api.permissions import IsOwnerOrReadOnly


class CategoryDestroyViewset(DestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]