from djangopost import views
from django.urls import include
from django.conf.urls import re_path

app_name = 'djangopost'

urlpatterns = [
    re_path(r'^api/', include('djangopost.rest_api.urls')),
    re_path(r'^article/dashboard/$', views.ArticleListDashboard, name='article_list_dashboard'),
    re_path(r'^article/create/$', views.ArticleCreateView, name='article_create_view'),
    re_path(r'^article/(?P<article_slug>[\w-]+)/$', views.ArticleDetailView, name='article_detail_view'),
    re_path(r'^article/(?P<article_slug>[\w-]+)/delete/$', views.ArticleDeleteView, name='article_delete_view'),
    re_path(r'^article/(?P<article_slug>[\w-]+)/update/$', views.ArticleUpdateView, name='article_update_view'),
    re_path(r'^category/dashboard/$', views.CategoryListDashboard, name='category_list_dashboard'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/delete/$', views.CategoryDeleteView, name='category_delete_view'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/update/$', views.CategoryUpdateView, name='category_update_view'),
    re_path(r'^category/create/$', views.CategoryCreateView, name='category_create_view'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/$', views.CategoryDetailView, name='category_detail_view'),
    re_path(r'^$', views.ArticleListView, name='article_list_view')
]