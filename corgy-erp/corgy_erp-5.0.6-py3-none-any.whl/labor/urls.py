from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./employment/'), name="index"),
    url('^salary/', include(views.SalaryModelViewSet().urls)),
    url('^employment/', include(views.EmploymentModelViewSet().urls)),
]