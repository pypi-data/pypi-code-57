from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from lionclaw.shipping.models import ShippingRate
from django.utils.translation import ugettext_lazy as _


class ShippingRateModelAdmin(ModelAdmin):
    model = ShippingRate
    menu_label = _('Shipping')
    menu_order = 200
    menu_icon = 'site'
    add_to_settings_menu = False
    exclude_from_explorer = True
    list_display = ('name', 'rate', 'carrier', 'description')


modeladmin_register(ShippingRateModelAdmin)
