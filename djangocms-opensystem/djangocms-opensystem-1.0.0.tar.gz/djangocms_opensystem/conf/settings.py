# Third party
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# django.utils.translation should never be imported from within a settings file!
# Instead use a fake _() function in order to mark the strings wrapped with _() for translation.
_ = lambda s: s  # noqa

BASKET_ID = getattr(settings, "DJANGOCMS_OPENSYSTEM_BASKET_ID", None)
if BASKET_ID is None:
    raise ImproperlyConfigured("DJANGOCMS_OPENSYSTEM_BASKET_ID must be defined")

INTEGRATION_ID = getattr(settings, "DJANGOCMS_OPENSYSTEM_INTEGRATION_ID", None)
if INTEGRATION_ID is None:
    raise ImproperlyConfigured("DJANGOCMS_OPENSYSTEM_INTEGRATION_ID must be defined")
