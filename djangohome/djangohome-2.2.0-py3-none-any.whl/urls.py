from django.conf.urls import re_path
from djangohome import views

app_name = 'djangohome'

urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='home_page_view')
]