from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from commons.models import Person
from masterdata.models import BusinessForm
from viewflow.models import Process
import uuid

# Create your models here.

class Customer(models.Model):
    """
    Ügyfél
    """
    class Meta:
        db_table = 'customers'
        verbose_name = _("ügyfél")
        verbose_name_plural = _("ügyfelek")

    name = models.CharField(
        verbose_name=_('megnevezés'),
        max_length=500,
        null=True,
        blank=True
    )

    @property
    def display_name(self):
        return self.name

    def __str__(self):
        return str(self.display_name)

class Individual(Customer):
    """
    Ügyfél: egyéni vállalkozás
    """
    class Meta:
        db_table = 'individuals'
        verbose_name = _("egyéni vállalkozás")
        verbose_name_plural = _("egyéni vállalkozások")

    prime_number = models.UUIDField(
        verbose_name=_('törzsszám'),
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )

    owner = models.ForeignKey(
        verbose_name=_("személyi adatok"),
        to=Person,
        related_name='persons',
        on_delete=models.CASCADE
    )

    @property
    def display_name(self):
        return str(self.owner)


class Organization(Customer):
    """
    Ügyfél: társas vállalkozás
    """
    class Meta:
        db_table = 'organizations'
        verbose_name = _("társas vállalkozás")
        verbose_name_plural = _("társas vállalkozások")

    prime_number = models.UUIDField(
        verbose_name=_('törzsszám'),
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    )

    manager = models.ForeignKey(
        verbose_name=_("ügyvezető"),
        to=Person,
        related_name='managers',
        on_delete=models.CASCADE
    )

    registration_number = models.CharField(
        verbose_name=_('cégjegyzékszám'),
        max_length=500,
        blank=False,
        null=False
    )

    business_form = models.ForeignKey(
        verbose_name=_('cégforma'),
        to=BusinessForm,
        related_name='organizations',
        on_delete=models.CASCADE
    )

    @property
    def display_name(self):
        return str(self.name)

    def __str__(self):
        return str(self.display_name)

class SubscriptionProcess(Process):

    class Meta:
        db_table = 'process_subscription'
        verbose_name = _("beléptetés")
        verbose_name_plural = _("beléptetések")

    customer = models.ForeignKey(
        verbose_name=_('vállalkozás'),
        to=Customer,
        on_delete=models.CASCADE
    )

class UnsubscriptionProcess(Process):

    class Meta:
        db_table = 'process_unsubscription'
        verbose_name = _("kiléptetés")
        verbose_name_plural = _("kiléptetések")

    customer = models.ForeignKey(
        verbose_name=_('vállalkozás'),
        to = Customer,
        on_delete = models.CASCADE
    )