from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from djangoarticle.models import ArticleModelScheme


class ArticleSchemeSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:article_retrieve_viewset",
        lookup_field = "slug"
    )

    api_update_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:article_update_viewset",
        lookup_field = "slug"
    )

    api_delete_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:article_destroy_viewset",
        lookup_field = "slug"
    )

    detail_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:article_detail_view",
        lookup_field = "slug",
        lookup_url_kwarg = "article_slug"
    )

    class Meta:
        model = ArticleModelScheme
        fields = ['serial', 'cover_image', 'title', 'slug', 'category', 'description', 'shortlines',
                  'content', 'author', 'status', 'verification', 'is_promote', 'is_trend',
                  'total_views', 'created_at', 'updated_at', 'api_detail_url', 'api_update_url',
                  'api_delete_url', 'detail_url']