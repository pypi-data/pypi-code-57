from rest_framework import routers
from .views import NodeViewSet


router = routers.DefaultRouter()
router.register('source',NodeViewSet)

urlpatterns = router.urls