"""Implementation of the middleware responsible for filtering released countries
to access the application."""

from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.conf import settings

from .provider import DjangoCountryFilterProvider


class DjangoCountryFilterMiddleware:
    """Django middleware to call the class responsible for setting up the provider call,
    which is DjangoCountryFilterProvider."""

    def __init__(self, get_response):
        """Middleware initializer."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """Checks the middleware settings and calls DjangoCountryFilterProvider."""
        response = self.get_response(request)
        if hasattr(settings, 'DJANGO_COUNTRY_FILTER_COUNTRIES'):
            if type(settings.DJANGO_COUNTRY_FILTER_COUNTRIES) is not list:
                raise Exception('DJANGO_COUNTRY_FILTER_COUNTRIES is not a list type.')
            else:
                res = DjangoCountryFilterProvider(request).get()
                if not res['country'] in settings.DJANGO_COUNTRY_FILTER_COUNTRIES:
                    return HttpResponseForbidden()
        return response
