from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import models as auth_models
from django.urls import path

from django_core_api import views

admin.autodiscover()

try:
    admin.site.unregister(auth_models.User)
    admin.site.unregister(auth_models.Group)
except NotRegistered:
    pass

admin.site.site_header = settings.SITE_NAME

urlpatterns = [
    path(r'healthcheck', views.HealthCheck.as_view()),

    path('admin/', admin.site.urls),
]
