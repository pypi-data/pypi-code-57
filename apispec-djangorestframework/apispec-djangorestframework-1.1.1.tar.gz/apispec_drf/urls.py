# encoding: utf-8


from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView


urlpatterns = [

    url(r'^(?P<version>[^/]+)/?$', TemplateView.as_view(template_name="apispec_drf/swagger-ui.html")),

]
