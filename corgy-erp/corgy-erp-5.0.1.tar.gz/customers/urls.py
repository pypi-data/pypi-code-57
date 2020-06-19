from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./all/'), name="index"),
    url('^organization/', include(views.OrganizationModelViewSet().urls)),
    url('^individual/', include(views.IndividualModelViewSet().urls)),
    url('^all/', include(views.CustomerModelViewSet().urls)),
]