from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("authors/", views.AuthorView.as_view(), name="author-list"),
    path("authors/<str:slug>/", views.AuthorManageView.as_view(), name="author-detail"),
    path(
        "social_accounts/",
        views.SocialAccountView.as_view(),
        name="social_account-list",
    ),
    path(
        "social_accounts/<str:slug>/",
        views.SocialAccountManageView.as_view(),
        name="social_account-detail",
    ),
    path("tags/", views.TagView.as_view(), name="tag-list"),
    path("tags/<str:slug>/", views.TagManageView.as_view(), name="tag-detail"),
    path("categories/", views.CategoryView.as_view(), name="category-list"),
    path(
        "categories/<str:slug>/",
        views.CategoryManageView.as_view(),
        name="category-detail",
    ),
    path("posts/", views.PostView.as_view(), name="post-list"),
    path("posts/<str:slug>/", views.PostManageView.as_view(), name="post-detail"),
]
