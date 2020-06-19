from rest_framework.generics import CreateAPIView
from djangopost.models import CategoryModel
from djangopost.rest_api.serializers import CategorySerializer


class CategoryCreateViewset(CreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer