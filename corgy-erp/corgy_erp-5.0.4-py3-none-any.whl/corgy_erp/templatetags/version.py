from django import template

register = template.Library()

@register.simple_tag()
def current_version():
    from ..version import __version__ as corgy_erp_version
    return corgy_erp_version