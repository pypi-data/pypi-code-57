from django.urls import path
from . import views

app_name = "easyaudit_utils"
urlpatterns = [
    path("events/index/", views.IndexView.as_view(), name="index"),
    path("events/crud/list/", views.CRUDEventListView.as_view(), name="crud_event_list"),
    path("events/login/list/", views.LoginEventListView.as_view(), name="login_event_list"),
    path("events/request/list/", views.RequestEventListView.as_view(), name="request_event_list"),
]
