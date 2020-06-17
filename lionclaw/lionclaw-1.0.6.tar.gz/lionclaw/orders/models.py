from datetime import datetime
from django.db import models
from lionclaw.settings import PRODUCT_VARIANT_MODEL
from lionclaw.shipping.models import Address
from django.utils.translation import ugettext_lazy as _

class Order(models.Model):
    SUBMITTED = 1
    FULFILLED = 2
    CANCELLED = 3
    REFUNDED = 4
    FAILURE = 5
    ORDER_STATUSES = ((SUBMITTED, _('Submitted')),
                      (FULFILLED, _('Fulfilled')),
                      (CANCELLED, _('Cancelled')),
                      (REFUNDED, _('Refunded')),
                      (FAILURE, _('Payment Failed')))
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Payment Date'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED, verbose_name=_('Order Status'))
    status_note = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Order Status Note'))

    transaction_id = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Transaction ID'))

    # contact info
    email = models.EmailField(max_length=128, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))

    # shipping info
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_shipping_address", on_delete=models.PROTECT, verbose_name=_('Shipping Address'))

    # billing info
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_billing_address", on_delete=models.PROTECT, verbose_name=_('Billing Address'))

    shipping_rate = models.DecimalField(max_digits=12,
                                        decimal_places=2,
                                        blank=True,
                                        null=True,
                                        verbose_name=_('Shipping Rate'))

    def __str__(self):
        return "Order #{} - {}".format(self.id, self.email)

    @property
    def total(self):
        """Total cost of the order
        """
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def total_items(self):
        """The number of individual items on the order
        """
        return self.items.count()


    def refund(self):
        """Issue a full refund for this order
        """
        from lionclaw.utils import GATEWAY
        now = datetime.strftime(datetime.now(), "%b %d %Y %H:%M:%S")
        if GATEWAY.issue_refund(self.transaction_id, self.total):
            self.status = self.REFUNDED
            self.status_note = "Refunded on {}".format(now)
        else:
            self.status_note = "Refund failed on {}".format(now)
        self.save()

    def fulfill(self):
        """Mark this order as being fulfilled
        """
        self.status = self.FULFILLED
        self.save()

    def cancel(self, refund=True):
        """Cancel this order, optionally refunding it
        """
        if refund:
            self.refund()
        self.status = self.CANCELLED
        self.save()

class OrderItem(models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.DO_NOTHING, verbose_name=_('Product'))
    quantity = models.IntegerField(default=1, verbose_name=_('Quantity'))
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_('Order'))

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())
