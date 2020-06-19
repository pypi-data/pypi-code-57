from django.conf.urls import re_path
from django.urls import include
from djangoarticle import views

app_name = 'djangoarticle'

urlpatterns = [
    re_path(r'^api/', include('djangoarticle.rest_api.urls')),
    re_path(r'^category/dashboard/$', views.CategoryListDashboard.as_view(), name='category_list_dashboard'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/delete/$', views.CategoryDeleteView.as_view(), name='category_delete_view'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/update/$', views.CategoryUpdateView.as_view(), name='category_update_view'),
    re_path(r'^category/create/$', views.CategoryCreateView.as_view(), name='category_create_view'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name='category_detail_view'),
    re_path(r'^article/dashboard/$', views.ArticleListDashboard.as_view(), name='article_list_dashboard'),
    re_path(r'^article/(?P<article_slug>[\w-]+)/delete/$', views.ArticleDeleteView.as_view(), name='article_delete_view'),
    re_path(r'^article/(?P<article_slug>[\w-]+)/update/$', views.ArticleUpdateView.as_view(), name='article_update_view'),
    re_path(r'^article/create/$', views.ArticleCreateView.as_view(), name='article_create_view'),
    re_path(r'^article/(?P<article_slug>[\w-]+)/$', views.ArticleDetailView.as_view(), name='article_detail_view'),
    re_path(r'^$', views.ArticleListView.as_view(), name='article_list_view')
]