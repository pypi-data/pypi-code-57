import jinja2
import jinja2.nodes
from jinja2.ext import Extension

from django.template.loader import get_template

from .templatetags.lionclawcheckout_tags import gateway_client_js, gateway_token


class LionClawCheckoutExtension(Extension):
    def __init__(self, environment):
        super(LionClawCheckoutExtension, self).__init__(environment)

        self.environment.globals.update({
            'gateway_client_js': gateway_client_js,
            'gateway_token': gateway_token
        })


# Nicer import names
checkout = LionClawCheckoutExtension
