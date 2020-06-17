from .views import send, verify
from django.urls import path

urlpatterns = [
    path('', send),
    path('<str:email>/<str:email_token>', verify)
]
