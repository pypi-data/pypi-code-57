from rest_framework.routers import DefaultRouter

from huscy.subjects import views


router = DefaultRouter()
router.register('addresses', views.AddressViewSet)
router.register('contacts', views.ContactViewSet)
router.register('phones', views.PhoneViewSet)
router.register('subjects', views.SubjectViewSet)

urlpatterns = router.urls
