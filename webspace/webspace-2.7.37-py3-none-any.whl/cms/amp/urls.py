from django.conf.urls import url
from wagtail.core.urls import serve_pattern

from . import views

urlpatterns = [
    url(serve_pattern, views.serve, name='wagtail_amp_serve')
]
