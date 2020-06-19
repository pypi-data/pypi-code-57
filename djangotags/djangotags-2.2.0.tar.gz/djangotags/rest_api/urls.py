from django.conf.urls import re_path, include
from djangotags.rest_api import viewsets


urlpatterns = [
    re_path(r'^tag/all/$', viewsets.TagListViewset.as_view(), name="tag_list_viewset"),
    re_path(r'^tag/(?P<tag_slug>[\w-]+)/$', viewsets.TagRetrieveViewset.as_view(), name="tag_retrieve_viewset"),
    re_path(r'^tag/(?P<tag_slug>[\w-]+)/update/$', viewsets.TagUpdateViewset.as_view(), name="tag_update_viewset"),
    re_path(r'^tag/(?P<tag_slug>[\w-]+)/delete/$', viewsets.TagDestroyViewset.as_view(), name="tag_destroy_viewset")
]