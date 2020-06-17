from django import template
from lionclaw.shipping.utils import get_shipping_cost
from lionclaw.configuration.models import Configuration


register = template.Library()

@register.simple_tag(takes_context=True)
def shipping_rate(context, **kwargs):
    """Return the shipping rate for a country & shipping option name.
    """
    settings = Configuration.for_site(context["request"].site)
    code = kwargs.get('code', None)
    name = kwargs.get('name', None)
    return get_shipping_cost(settings, code, name)
