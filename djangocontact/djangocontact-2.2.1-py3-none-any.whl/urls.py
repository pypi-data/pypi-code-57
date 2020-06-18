from django.urls.conf import re_path
from djangocontact import views

app_name = 'djangocontact'

urlpatterns = [
    re_path(r'^contact-us/$', views.EmailContactView, name='email_contact_view')
]