from django.urls import path
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "web/home.html"


app_name = "web"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
