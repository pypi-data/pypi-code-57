import os
from django import template
from lionclaw import settings

register = template.Library()

CLIENT_PATH = os.path.join('core', 'js', 'lionclawclient.bundle.js')
VENDORS_PATH = os.path.join('core', 'js', 'vendors.bundle.js')

@register.inclusion_tag("core/script.html")
def longclaw_vendors_bundle():
    assert os.path.exists(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', VENDORS_PATH)
    )
    return {'path': VENDORS_PATH}

@register.inclusion_tag("core/script.html")
def lionclaw_client_bundle():
    assert os.path.exists(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', CLIENT_PATH)
    )
    return {'path': CLIENT_PATH}

@register.simple_tag
def lionclaw_api_url_prefix():
    return settings.API_URL_PREFIX


