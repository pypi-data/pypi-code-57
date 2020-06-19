from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from taggit.models import Tag


class TagSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(
        view_name = "djangotags:tag_retrieve_viewset",
        lookup_field = "slug",
        lookup_url_kwarg = "tag_slug"
    )

    api_update_url = HyperlinkedIdentityField(
        view_name = "djangotags:tag_update_viewset",
        lookup_field = "slug",
        lookup_url_kwarg = "tag_slug"
    )

    api_delete_url = HyperlinkedIdentityField(
        view_name = "djangotags:tag_destroy_viewset",
        lookup_field = "slug",
        lookup_url_kwarg = "tag_slug"
    )

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'api_detail_url', 'api_update_url', 'api_delete_url']