from rest_framework.generics import ListAPIView
from taggit.models import Tag
from djangotags.rest_api.serializers import TagSerializer


class TagListViewset(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer