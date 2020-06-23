"""URLs provided by this application.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DevicesViewset

router = DefaultRouter()
router.register(r'devices', DevicesViewset, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
]
