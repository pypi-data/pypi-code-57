from django.conf.urls import url

from remo_app.remo.api.views.docs import serve_docs

urlpatterns = [
    url(r'^(?P<path>.*)$', serve_docs),
]
