from django.urls import path
from .views_admin import index, build


urlpatterns = [
    path('', index, name="index"),
    path('build', build, name="build"),
]
