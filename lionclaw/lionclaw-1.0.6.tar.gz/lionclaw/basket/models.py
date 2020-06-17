from django.db import models
from lionclaw.settings import PRODUCT_VARIANT_MODEL
from django.utils.translation import ugettext_lazy


class BasketItem(models.Model):
    basket_id = models.CharField(max_length=32, verbose_name=ugettext_lazy('Basket ID'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=ugettext_lazy('Date Added'))
    quantity = models.IntegerField(default=1, verbose_name=ugettext_lazy('Quantity'))
    variant = models.ForeignKey(PRODUCT_VARIANT_MODEL, unique=False, on_delete=models.PROTECT,
                                verbose_name=ugettext_lazy('Variant'))

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return "{}x {}".format(self.quantity, self.variant)

    def total(self):
        return self.quantity * self.variant.price

    def name(self):
        return self.variant.__str__()

    def price(self):
        return self.variant.price

    def increase_quantity(self, quantity=1):
        """ Increase the quantity of this product in the basket
        """
        self.quantity += quantity
        self.save()

    def decrease_quantity(self, quantity=1):
        """
        """
        self.quantity -= quantity
        if self.quantity <= 0:
            self.delete()
        else:
            self.save()
