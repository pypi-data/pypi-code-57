from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()

@register.filter()
def url_name(model, action):
    """
    Return the URL name for the given model and action, or None if invalid.
    """
    url_name = 'plugins:{}:{}_{}'.format(model._meta.app_label, model._meta.model_name, action)
    return url_name
