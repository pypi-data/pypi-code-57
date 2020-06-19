from djangoarticle.rest_api import viewsets as views 
from django.conf.urls import re_path


urlpatterns = [
    # urlpatterns for article api.
    re_path(r'^article/all/$', views.ArticleListViewset.as_view(), name='article_list_viewset'),
    re_path(r'^article/published/$', views.ArticleListPublishedViewset.as_view(), name='article_list_published_viewset'),
    re_path(r'^article/promoted/$', views.ArticleListPromotedViewset.as_view(), name='article_list_promoted_viewset'),
    re_path(r'^article/trending/$', views.ArticleListTrendingViewset.as_view(), name='article_list_trending_viewset'),
    re_path(r'^article/promo/$', views.ArticleListPromoViewset.as_view(), name='article_list_promo_viewset'),
    re_path(r'^article/create/$', views.ArticleCreateViewset.as_view(), name='article_create_viewset'),
    re_path(r'^article/(?P<slug>[\w-]+)/$', views.ArticleRetrieveViewset.as_view(), name='article_retrieve_viewset'),
    re_path(r'^article/(?P<slug>[\w-]+)/update/$', views.ArticleUpdateViewset.as_view(), name='article_update_viewset'),
    re_path(r'^article/(?P<slug>[\w-]+)/destroy/$', views.ArticleDestroyViewset.as_view(), name='article_destroy_viewset'),
    # urlpatterns for category api.
    re_path(r'^category/all/$', views.CategoryListViewset.as_view(), name='category_list_viewset'),
    re_path(r'^category/published/$', views.CategoryListPublishedViewset.as_view(), name='category_list_published_viewset'),
    re_path(r'^category/create/$', views.CategoryCreateViewset.as_view(), name='category_create_viewset'),
    re_path(r'^category/(?P<slug>[\w-]+)/$', views.CategoryRetrieveViewset.as_view(), name='category_retrieve_viewset'),
    re_path(r'^category/(?P<slug>[\w-]+)/update/$', views.CategoryUpdateViewset.as_view(), name='category_update_viewset'),
    re_path(r'^category/(?P<slug>[\w-]+)/destroy/$', views.CategoryDestroyViewset.as_view(), name='category_destroy_viewset'),            
    # urlpatterns for category-detail article-list api.
    re_path(r'^category/detail/(?P<slug>[\w-]+)/$', views.CategoryDetailArticleListViewset.as_view(), name='category_detail_article_list_viewset'),
    # urlpatterns for taggit-detail article-list api.
    re_path(r'^tag/detail/(?P<slug>[\w-]+)/$', views.TaggitDetailArticleListViewset.as_view(), name='taggit_detail_article_list_viewset')
]