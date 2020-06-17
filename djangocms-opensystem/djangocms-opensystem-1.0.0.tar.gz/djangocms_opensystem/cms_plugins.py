from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from models import WidgetConfig
from conf.settings import INTEGRATION_ID, BASKET_ID


class OpenSystemPlugin(CMSPluginBase):
    model = WidgetConfig
    name = _("OpenSystem widget")
    render_template = "djangocms_opensystem/widget.html"

    def render(self, context, instance, placeholder):
        context.update({
            "object": instance,
            "BASKET_ID": BASKET_ID,
            "INTEGRATION_ID": INTEGRATION_ID,
            "placeholder": placeholder,
        })
        return context

plugin_pool.register_plugin(OpenSystemPlugin)
