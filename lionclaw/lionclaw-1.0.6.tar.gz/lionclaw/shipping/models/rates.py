from django.db import models
from django.dispatch import receiver

from lionclaw.basket.signals import basket_modified
from wagtail.admin.edit_handlers import FieldPanel
from django.utils.translation import ugettext_lazy as _

from ..signals import address_modified


class ShippingRate(models.Model):
    """
    An individual shipping rate. This can be applied to
    multiple countries.
    """
    name = models.CharField(
        max_length=32,
        unique=True,
        help_text=_("Unique name to refer to this shipping rate by")
    )
    rate = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Shipping Rate'))
    carrier = models.CharField(max_length=64, verbose_name=_('Carrier'))
    description = models.CharField(max_length=128, verbose_name=_('Description'))
    countries = models.ManyToManyField('shipping.Country', verbose_name=_('Shipping Country'))
    basket_id = models.CharField(blank=True, db_index=True, max_length=32, verbose_name=_('Basket ID'))
    destination = models.ForeignKey('shipping.Address', blank=True, null=True, on_delete=models.PROTECT, verbose_name=_('Destination'))
    processor = models.ForeignKey('shipping.ShippingRateProcessor', blank=True, null=True, on_delete=models.PROTECT)

    panels = [
        FieldPanel('name'),
        FieldPanel('rate'),
        FieldPanel('carrier'),
        FieldPanel('description'),
        FieldPanel('countries')
    ]

    def __str__(self):
        return self.name


@receiver(address_modified)
def clear_address_rates(sender, instance, **kwargs):
    ShippingRate.objects.filter(destination=instance).delete()


@receiver(basket_modified)
def clear_basket_rates(sender, basket_id, **kwargs):
    ShippingRate.objects.filter(basket_id=basket_id).delete()
