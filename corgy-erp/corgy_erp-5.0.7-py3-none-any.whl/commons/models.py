from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.timezone import timezone, timedelta, datetime, now
from django.contrib.auth.models import User
#from userprofile.models import AbstractSubscriptionProfile
from address.models import AddressField, Address
from phonenumber_field.modelfields import PhoneNumberField
import uuid
# Create your models here.

# class MyModel(models.Model):
#     name = models.CharField(max_length=250)

class MasterDataMixin(models.Model):
    class Meta:
        abstract = True

    code = models.CharField(
        verbose_name=_("kód"),
        max_length=100,
        blank=True,
        null=True,
        default=None
    )

    name = models.CharField(
        verbose_name=_("megnevezés"),
        max_length=1000,
        blank=True,
        null=True,
        default=None
    )

    def __str__(self):
        return self.name

class IntervalMixin(models.Model):
    class Meta:
        abstract = True

    begin = models.DateField(
        verbose_name=_("kezdet"),
        default=None,
        blank=True,
        null=True
    )

    end = models.DateField(
        verbose_name=_("vég"),
        default=None,
        blank=True,
        null=True
    )


gender_female = 'female'
gender_male = 'male'
gender_choices = [
    (gender_female, _('Nő')),
    (gender_male, _('Férfi')),
]

def current_month_generator():
    return now().month

def current_year_generator():
    return now().year

class MonthBasedMixin(models.Model):

    class Meta:
        abstract = True

    current_month = models.PositiveSmallIntegerField(
        verbose_name=_('tárgyhó'),
        default=current_month_generator
    )

    current_year = models.PositiveIntegerField(
        verbose_name=_('tárgyév'),
        default=current_year_generator
    )

    @property
    def started(self) -> datetime:
        return datetime(
            year=self.current_year,
            month=self.current_month,
            day=1
        )

    @property
    def ended(self) -> datetime:
        return self.started.replace(day=calendar.monthlen(self.current_year, self.current_month))

class Person(models.Model):
    """
    Személyi adatlap
    """
    class Meta:
        db_table = 'persons'
        verbose_name = _("személy")
        verbose_name_plural = _("személyek")

    gender = models.CharField(
        verbose_name=_('nem'),
        choices=gender_choices,
        max_length=10,
        default=None,
        blank=True,
        null=True,
    )

    birthdate = models.DateField(
        verbose_name=_('születési dátum'),
        blank=False,
        null=False,
    )

    birthplace = models.CharField(
        verbose_name=_('születési hely'),
        max_length=200,
        blank=False,
        null=False
    )

    name_of_mother = models.CharField(
        verbose_name=_('anyja neve'),
        max_length=200,
        default=None,
        blank=False,
        null=False
    )

    first_name = models.CharField(
        verbose_name=_('keresztnév'),
        max_length=100,
        blank=False,
        null=False
    )

    middle_name = models.CharField(
        verbose_name=_('középső név'),
        max_length=100,
        default=None,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        verbose_name=_('családnév'),
        max_length=100,
        blank=False,
        null=False
    )

    permanent_address = AddressField(
        verbose_name=_('állandó lakcím'),
        related_name='permanent_residents',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    temporary_address = AddressField(
        verbose_name=_('ideiglenes lakcím'),
        related_name='termorary_residents',
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE
    )

    phone_number = PhoneNumberField(
        verbose_name=_('telefonszám'),
        blank=False,
        null=False,
    )

    email = models.EmailField(
        verbose_name=_('email cím'),
    )

    nationality = models.CharField(
        verbose_name=_('nemzetiség'),
        max_length=100
    )

    inland_resident = models.BooleanField(
        verbose_name=_('belföldi lakcím'),
        help_text=_('Rendelkezik belföldi lakcímmel.'),
        blank=False,
        null=False,
        default=True
    )

    tax_number = models.CharField(
        verbose_name=_('adó azonosító jel'),
        max_length=100
    )

    @property
    def full_name(self):
        return "{first} {middle} {last}".format(
            first=str(self.first_name) if self.first_name is not None else '',
            middle=str(self.middle_name) if self.middle_name is not None else '',
            last=str(self.last_name if self.last_name is not None else '')
        ).title()

    def __str__(self):
        return str(self.full_name)
#
# class Account(AbstractSubscriptionProfile, models.Model):
#      """
#      Felhasználói fiók
#      """
#      class Meta:
#          db_table = 'accounts'
#          verbose_name = _("felhasználói fiók")
#          verbose_name_plural = _("felhasználói fiókok")