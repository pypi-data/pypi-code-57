from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./profile/'), name="index"),
    url('^profile/', include(views.ProfileModelViewSet().urls)),
]