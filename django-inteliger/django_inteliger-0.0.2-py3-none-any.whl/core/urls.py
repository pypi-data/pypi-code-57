from django.urls import re_path
from core.views import InteligerView

urlpatterns = [
    re_path(r'^atualizar$', InteligerView.as_view(), name='sistema_atualizar'),
]
