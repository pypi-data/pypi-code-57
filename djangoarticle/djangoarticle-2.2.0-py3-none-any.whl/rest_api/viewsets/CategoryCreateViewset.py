from rest_framework.generics import CreateAPIView
from djangoarticle.models import CategoryModelScheme
from djangoarticle.rest_api.serializers import CategorySchemeSerializer


class CategoryCreateViewset(CreateAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer