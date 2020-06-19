from rest_framework.generics import RetrieveAPIView
from taggit.models import Tag
from djangotags.rest_api.serializers import TagSerializer


class TagRetrieveViewset(RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "tag_slug"