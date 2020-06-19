from django.conf.urls import url
from sbc_drf.routers import ExtendedSimpleRouter

from . import views

router = ExtendedSimpleRouter()
extra_url = [url(r'actions/password_reset', views.password_reset)]
user_router = router.register(r'^', views.UserViewSet)

urlpatterns = router.urls + extra_url
