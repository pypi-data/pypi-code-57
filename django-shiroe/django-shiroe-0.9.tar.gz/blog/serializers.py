from django.utils.text import slugify
from rest_framework import serializers
from .models import Author, SocialAccount, Post, Tag, Category


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model"""

    class Meta:
        model = Author
        fields = ("user", "first_name", "last_name", "slug", "description")
        read_only_fields = ("slug",)


class SocialAccountSerializer(serializers.ModelSerializer):
    """Serializer for Social Account model"""

    class Meta:
        model = SocialAccount
        fields = (
            "name",
            "url",
            "slug",
        )
        read_only_fields = ("slug",)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model """

    class Meta:
        model = Tag
        fields = (
            "name",
            "slug",
        )
        read_only_fields = ("slug",)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model """

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )
        read_only_fields = ("slug",)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model """

    tags = serializers.SlugRelatedField(
        many=True, required=False, queryset=Tag.objects.all(), slug_field="slug",
    )

    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "content",
            "summary",
            "status",
            "category",
            "file_type",
            "tags",
        )
        read_only_fields = ("slug",)


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post model """

    tags = serializers.SlugRelatedField(
        many=True,
        required=False,
        allow_empty=True,
        queryset=Tag.objects.all(),
        slug_field="slug",
    )

    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "content",
            "summary",
            "status",
            "category",
            "file_type",
            "tags",
        )
        read_only_fields = ("slug", "title", "content")


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to posts """

    class Meta:
        model = Post
        fields = ("slug", "cover_image")
        read_only_fields = ("slug",)
