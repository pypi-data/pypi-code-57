from django.urls import path
from . import views

urlpatterns = [
    # A simple test page
    path('sample', views.index, name='sample'),
    path('upload', views.upload_file, name='upload_file'),
]
