from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent

from .mixins import PaginationMixin, UserDateSearchMixin


class IndexView(LoginRequiredMixin, UserDateSearchMixin, TemplateView):
    template_name = "easyaudit/index.html"


class CRUDEventListView(LoginRequiredMixin, PaginationMixin, UserDateSearchMixin, ListView):
    model = CRUDEvent
    paginate_by = 50


class LoginEventListView(LoginRequiredMixin, PaginationMixin, UserDateSearchMixin, ListView):
    model = LoginEvent  # TODO : Use Django-defender
    paginate_by = 50


class RequestEventListView(LoginRequiredMixin, PaginationMixin, UserDateSearchMixin, ListView):
    model = RequestEvent
    paginate_by = 50
