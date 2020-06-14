from django.conf.urls import url
from .views import csrf_token

urlpatterns = [
    url(r'^csrf_token/$', csrf_token, name='csrf_token')
]

