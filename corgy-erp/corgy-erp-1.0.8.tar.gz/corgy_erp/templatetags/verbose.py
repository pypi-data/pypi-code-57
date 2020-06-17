from django import template

register = template.Library()

@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Returns verbose_name for a model.
    """
    return instance._meta.verbose_name.title()