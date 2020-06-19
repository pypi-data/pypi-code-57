from django.conf.urls import re_path, include
from djangotags import views

app_name = "djangotags"

urlpatterns = [
    re_path(r'^api/', include("djangotags.rest_api.urls")),
    re_path(r'^(?P<tag_slug>[\w-]+)/$', views.TaggitTagDetailView.as_view(), name="taggit_tag_detail_view")
]