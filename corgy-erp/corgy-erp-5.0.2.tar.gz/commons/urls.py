from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
   url('^$', generic.RedirectView.as_view(url='./person/'), name="index"),
   url('^person/', include(views.PersonModelViewSet().urls)),
]