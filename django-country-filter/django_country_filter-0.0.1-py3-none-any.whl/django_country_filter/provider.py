"""Class factory for providers that will be used to verify the IP addresses of requests."""

import importlib

from django.conf import settings


class DjangoCountryFilterProvider:
    """Class factory for providers."""

    def _get_imported_provider(self, request):
        """Returns a provider according to the provider creation conventions."""
        module = settings.DJANGO_COUNTRY_FILTER_PROVIDER
        name = module.title().replace('_', '')
        provider = importlib.import_module(
            'django_country_filter.providers.{}'.format(module)
        )
        return getattr(provider, name)(request)

    def __init__(self, request):
        """Class initializer."""
        if not hasattr(settings, 'DJANGO_COUNTRY_FILTER_PROVIDER'):
            raise Exception('DJANGO_COUNTRY_FILTER_PROVIDER is not defined.')
        try:
            self.provider = self._get_imported_provider(request)
        except Exception:
            raise Exception('Error on provider building: Provider not found.')

    def get(self):
        """Calls the get method of the built provider."""
        return self.provider.get()
