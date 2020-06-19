from rest_framework.generics import RetrieveAPIView
from djangopost.models import CategoryModel
from djangopost.rest_api.serializers import CategorySerializer


class CategoryRetrieveViewset(RetrieveAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'