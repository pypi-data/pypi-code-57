from rest_framework.generics import RetrieveAPIView
from djangoarticle.models import CategoryModelScheme
from djangoarticle.rest_api.serializers import CategorySchemeSerializer


class CategoryRetrieveViewset(RetrieveAPIView):
    queryset = CategoryModelScheme.objects.all()
    serializer_class = CategorySchemeSerializer
    lookup_field = 'slug'