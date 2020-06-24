from django.conf.urls import url
from django.urls import include, path
from django.views import generic
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'businessform', views.BusinessFormApiViewSet)
router.register(r'contribution', views.ContributionApiViewSet)
router.register(r'discount', views.DiscountApiViewSet)
router.register(r'legal', views.LegalApiViewSet)
router.register(r'pretence', views.PretenceApiViewSet)
router.register(r'tax', views.TaxApiViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    url('^$', generic.RedirectView.as_view(url='./business_form/'), name="index"),
    url('^business_form/', include(views.BusinessFormModelViewSet().urls)),
    url('^legal/', include(views.LegalModelViewSet().urls)),
    url('^pretence/', include(views.PretenceModelViewSet().urls)),
    url('^tax/', include(views.TaxModelViewSet().urls)),
    url('^discount/', include(views.DiscountModelViewSet().urls)),
    url('^category/pause/', include(views.PauseCategoryModelViewSet().urls)),
    url('^category/timesheet/', include(views.TimeSheetCategoryModelViewSet().urls)),
]