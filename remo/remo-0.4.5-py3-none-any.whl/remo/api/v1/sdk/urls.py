from django.conf.urls import url, include
from rest_framework_nested import routers

from remo_app.remo.api.v1.sdk.handlers.dataset_images import DatasetImages
from remo_app.remo.api.v1.sdk.handlers.images import Images

router = routers.DefaultRouter()

router.register(r'images', Images, basename='images')
router.register(r'datasets', DatasetImages, basename='datasets')

urlpatterns = [
    url(r'^', include(router.urls)),
]
