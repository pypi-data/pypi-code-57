from rest_framework.generics import RetrieveUpdateAPIView
from djangopost.models import CategoryModel
from djangopost.rest_api.serializers import CategorySerializer
from djangopost.rest_api.permissions import IsOwnerOrReadOnly


class CategoryUpdateViewset(RetrieveUpdateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]