from django.db import models
from django.utils.translation import ugettext_lazy as _
from commons.models import MonthBasedMixin, IntervalMixin
from django.utils import timezone
from django.utils.timezone import timezone, timedelta, datetime, now
from commons.models import Person
from customers.models import Customer
from masterdata import models as mdm
from viewflow.models import Process
from commons.managers import TemporalQuerySet
import calendar
from django.utils import timezone

from django.db.models import Avg, Count, Min, Sum
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

class TimeSheet(models.Model):
    class Meta:
        db_table = 'timesheets'
        verbose_name = _("jelenléti ív")
        verbose_name_plural = _("jelenléti ívek")

    current_year = models.PositiveIntegerField(
        verbose_name=_("tárgyév"),
    )
    current_month = models.PositiveSmallIntegerField(
        verbose_name=_("tárgyhó"),
    )

    @property
    def current_workdays(self) -> int:
        return 20

    def prepare(self):
        for presence_type in mdm.TimeSheetCategory.objects.all():
            TimeSheetStatistic.objects.create(category=presence_type, sheet=self)
        for absence_type in mdm.PauseCategory.objects.all():
            AbsenseStatistic.objects.create(category=absence_type, sheet=self)

    def summarize(self):
        [presence_stat.close() for presence_stat in TimeSheetStatistic.objects.filter(sheet=self)]
        [absence_stat.close() for absence_stat in AbsenseStatistic.objects.filter(sheet=self)]

    def __str__(self):
        return '{year}/{month}'.format(year=self.current_year, month=calendar.month_name[self.current_month])

class TimeSheetItem(models.Model):
    sheet = models.ForeignKey(
        verbose_name=_("jelenléti"),
        to=TimeSheet,
        related_name='items',
        on_delete=models.CASCADE,
    )
    presence = models.ForeignKey(
        verbose_name=_("típus"),
        to=mdm.TimeSheetCategory,
        related_name='sheets',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    absence = models.ForeignKey(
        verbose_name=_("típus"),
        to=mdm.PauseCategory,
        related_name='sheets',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    timestamp = models.DateField(
        verbose_name=_("dátum")
    )
    duration = models.DurationField(
        verbose_name=_("munkaórák")
    )

class TimeSheetStatistic(models.Model):
    sheet = models.ForeignKey(
        verbose_name=_("jelenléti"),
        to=TimeSheet,
        related_name='presences',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        verbose_name=_("kategória"),
        to=mdm.TimeSheetCategory,
        related_name='presences',
        on_delete=models.CASCADE,
    )
    value = models.DurationField(
        blank=True,
        null=True,
        default=None
    )

    @property
    def calculate(self) -> timezone.timedelta:
        return TimeSheetItem.objects.filter(
            sheet=self.sheet,
            presence=self.category
        ).aggregate(Sum('duration'))

    def close(self):
        self.value = self.calculate


class AbsenseStatistic(models.Model):
    sheet = models.ForeignKey(
        verbose_name=_("jelenléti"),
        to=TimeSheet,
        related_name='absenses',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        verbose_name=_("kategória"),
        to=mdm.PauseCategory,
        related_name='absences',
        on_delete=models.CASCADE,
    )
    value = models.DurationField(
        blank=True,
        null=True,
        default=None
    )

    @property
    def calculate(self) -> timezone.timedelta:
        return TimeSheetItem.objects.filter(
            sheet=self.sheet,
            absence=self.category
        ).aggregate(Sum('duration'))

    def close(self):
        self.value = self.calculate


class Salary(IntervalMixin, models.Model):

    class Meta:
        db_table = 'salaries'
        ordering = ['-begin']
        verbose_name = _("bér")
        verbose_name_plural = _("bérek")

    objects = TemporalQuerySet.as_manager()

    employee = models.ForeignKey(
        verbose_name=_('munkavállaló'),
        related_name='salaries',
        to=Employment,
        on_delete=models.CASCADE,
    )

    timesheet = models.ForeignKey(
        verbose_name=_('jelenléti ív'),
        to=TimeSheet,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    salary = models.IntegerField(
        verbose_name=_('munkabér')
    )

    def period_year(self):
        return self.begin.year
    period_year.short_description = _('Tárgyév')

    def period_month(self):
        return calendar.month_name[self.begin.month]
    period_month.short_description = _('Tárgyhó')

    def summary(self):
        return self.salary
    summary.short_description = _('Összes járandóság')

    def non_monetary(self):
        return self.salary
    non_monetary.short_description = _('Nem pénzbeni járandóság')

    def pay(self):
        return self.salary
    pay.short_description = _('Fizetendő')

    def subtraction(self):
        return self.blocked.all().aggregate(Sum('value'))['value__sum']
    subtraction.short_description = _('Levonás')

    def transferred(self):
        return 0
    transferred.short_description = _('Átutalás')

    def cash(self):
        return 0
    cash.short_description = _('Készpénz')

    def __str__(self):
        return "{} - {}".format(self.employee, self.salary)

class BankAccount(models.Model):
    class Meta:
        db_table = 'bank_accounts'
        verbose_name = _('bankszámla')
        verbose_name_plural = _('bankszámlák')

    beneficiary = models.CharField(
        verbose_name=_('Kedvezményezett neve'),
        max_length=500
    )

    account_number = models.CharField(
        verbose_name=_('Bankszámlaszám'),
        max_length=500
    )

ATTRIBUTE_TYPE_CHOICES = [
    ('percent', _('Százalékos')),
    ('value', _('Érték szerint')),
]

class SalaryBlockingItem(models.Model):
    """
    Letiltás tétel
    """
    class Meta:
        db_table = 'salary_blocking_items'
        verbose_name = _('letiltás')
        verbose_name_plural = _('letiltások')

    salary = models.ForeignKey(
        to=Salary,
        related_name='blocked',
        on_delete=models.CASCADE,
    )

    value = models.FloatField(
        verbose_name=_('Összeg'),
        null=True,
        blank=True,
        default=None,
    )

    percent = models.FloatField(
        verbose_name=_('Százalék'),
        null=True,
        blank=True,
        default=None,
    )

    account = models.ForeignKey(
        to=BankAccount,
        on_delete=models.CASCADE,
    )

    attribute_type = models.CharField(
        verbose_name=_('Típus'),
        choices=ATTRIBUTE_TYPE_CHOICES,
        default='value',
        max_length=100,
    )

    def summary(self):
        return self.value if self.attribute_type == 'value' else self.salary.salary * self.percent
    summary.short_description = _('Összeg')

    def in_percent(self):
        if self.attribute_type == 'value':
            return self.salary.salary / self.value
        else:
            return self.percent
    in_percent.short_description = _('Százalékban')

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
        related_name='providers',
        on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        to=Employment,
        verbose_name=_('eltartó'),
        related_name='dependents',
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

    timesheet = models.ForeignKey(
        verbose_name=_('alkalmazott'),
        to=TimeSheet,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )

    submitted = models.NullBooleanField(
        verbose_name=_('elküldve'),
        help_text=_('hatóság felé elküldve')
    )