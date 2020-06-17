import jinja2
import jinja2.nodes
from jinja2.ext import Extension

from django.template.loader import get_template

# to keep namespaces from colliding
from .templatetags import lionclawcore_tags as lc_tags


def lionclaw_vendors_bundle():
    template = get_template('core/lionclaw_script.html')

    context = lc_tags.lionclaw_vendors_bundle()

    return template.render(context=context)


def lionclaw_client_bundle():
    template = get_template('core/lionclaw_script.html')

    context = lc_tags.lionclaw_client_bundle()

    return template.render(context=context)


class LionClawCoreExtension(Extension):
    def __init__(self, environment):
        super(LionClawCoreExtension, self).__init__(environment)

        self.environment.globals.update({
            'lionclaw_api_url_prefix': lc_tags.lionclaw_api_url_prefix,
            'lionclaw_client_bundle': lionclaw_client_bundle,
            'lionclaw_vendors_bundle': lionclaw_vendors_bundle,
        })


# Nicer import names
core = LionClawCoreExtension
