from django.db import models
from django.utils.translation import ugettext_lazy as _
from commons.models import MonthBasedMixin, IntervalMixin
from django.utils import timezone
from django.utils.timezone import timezone, timedelta, datetime, now
from commons.models import Person
from customers.models import Customer
from masterdata import models as mdm
from viewflow.models import Process
# Create your models here.

# class MyModel(models.Model):
#     name = models.CharField(max_length=250)

class Employment(IntervalMixin, Process):

    class Meta:
        db_table = 'employments'
        verbose_name = _("alkalmazott")
        verbose_name_plural = _("alkalmazottak")

    employee = models.ForeignKey(
        verbose_name=_('munkavállaló'),
        to=Person,
        on_delete=models.CASCADE
    )

    employer = models.ForeignKey(
        verbose_name=_('foglalkoztató'),
        to=Customer,
        on_delete=models.CASCADE
    )

    type = models.ForeignKey(
        verbose_name=mdm.ApplianceQuality._meta.verbose_name,
        to=mdm.ApplianceQuality,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return str(self.employee)


class Dependence(IntervalMixin, models.Model):
    """
    Eltartás
    """
    class Meta:
        db_table = 'dependents'
        verbose_name = _('eltartott')
        verbose_name_plural = _('eltartottak')

    dependent = models.ForeignKey(
        to=Person,
        verbose_name=_('eltartott'),
        related_name='dependents',
        on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        to=Employment,
        verbose_name=_('eltartó'),
        related_name='providers',
        on_delete=models.CASCADE
    )
    quality = models.ForeignKey(
        to=mdm.DependentQuality,
        verbose_name=mdm.DependentQuality._meta.verbose_name,
        on_delete=models.CASCADE
    )
    right = models.ForeignKey(
        to=mdm.DependentRight,
        verbose_name=mdm.DependentRight._meta.verbose_name,
        on_delete=models.CASCADE
    )


class PayrollManager(models.Manager):

    def create(self, employee, year=None, month=None):
        super().create(
            employee=employee,
            year=year if year is not None else now().year,
            month=None if month is not None else now().month,
        )

class Payroll(MonthBasedMixin, Process):

    class Meta:
        db_table = 'payrolls'
        verbose_name = _("bérszámfejtés")
        verbose_name_plural = _("bérszámfejtések")

    objects = PayrollManager()

    employee = models.ForeignKey(
        verbose_name=_('alkalmazott'),
        to=Employment,
        on_delete=models.CASCADE
    )

    employer = models.ForeignKey(
        verbose_name=_('foglalkoztató'),
        to=Customer,
        on_delete=models.CASCADE
    )

    submitted = models.NullBooleanField(
        verbose_name=_('elküldve'),
        help_text=_('hatóság felé elküldve')
    )