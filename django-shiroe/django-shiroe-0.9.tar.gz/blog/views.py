from django.http import Http404
from django.utils.text import slugify
from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Author, SocialAccount, Post, Tag, Category
from . import serializers


class AuthorView(generics.ListCreateAPIView):
    """Serializer for Author model"""

    serializer_class = serializers.AuthorSerializer
    queryset = Author.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class AuthorManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AuthorSerializer
    queryset = Author.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            return Author.objects.get(slug=slug)
        except Author.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SocialAccountView(generics.ListCreateAPIView):
    """Serializer for Author model"""

    serializer_class = serializers.SocialAccountSerializer
    queryset = SocialAccount.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class SocialAccountManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SocialAccountSerializer
    queryset = SocialAccount.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            return SocialAccount.objects.get(slug=slug)
        except SocialAccount.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryView(generics.ListCreateAPIView):
    """Serializer for Author model"""

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class CategoryManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TagView(generics.ListCreateAPIView):
    """Serializer for Author model"""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class TagManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostBaseView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        slug = self.kwargs.get("slug")
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404

    def _params_to_slug(self, qs):
        """Convert a list of names to a list of slugified names """
        return [slugify(q) for q in qs.split(",")]

    def get_queryset(self):
        """Get a recipe for an authenticated user"""
        tags = self.request.query_params.get("tags")
        queryset = self.queryset
        if tags:
            tags_slugs = self._params_to_slug(tags)
            queryset = queryset.filter(tags__slug__in=tags_slugs)
        return queryset.order_by("-title")


class PostView(generics.ListCreateAPIView):
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class PostManageView(PostBaseView):
    """Manage recipes in the database """

    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, slug=None):
        """Upload an image to a recipe """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        data_tags = list(filter(None, dict(request.data).get("tags") or []))
        if len(data_tags):
            for tag in data_tags:
                Tag.objects.get_or_create(name=tag, slug=slugify(tag))
        return super().partial_update(request, *args, **kwargs)
