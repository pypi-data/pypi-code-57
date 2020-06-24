from django.db import models
from commons.models import MasterDataMixin
from commons.models import IntervalMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Avg, Count, Min, Sum

# Create your models here.


class ApplianceQuality(MasterDataMixin, models.Model):
    """
    Alkalmazás minősége törzs
    """
    class Meta:
        db_table = 'appliance_qualitites'
        verbose_name = _('Alkalmazás minősége')
        verbose_name_plural = _('Alkalmazás minőségek')

class AutonomeActivityStatement(MasterDataMixin, models.Model):
    """
    Önálló tevékenység nyilatkozat törzs
    """
    class Meta:
        db_table = 'autotonome_activity_statements'
        verbose_name = _('Önálló tevékenység nyilatkozat')
        verbose_name_plural = _('Önálló tevékenység nyilatkozatok')


class BusinessForm(MasterDataMixin, models.Model):
    """
    Cégforma törzs
    """
    class Meta:
        db_table = 'business_forms'
        verbose_name = _('cégforma')
        verbose_name_plural = _('cégformák')


class Contribution(MasterDataMixin, models.Model):
    """
    Járulék törzs
    """
    class Meta:
        db_table = 'contributions'
        verbose_name = _("járulék")
        verbose_name_plural = _("járulékok")


class DependentQuality(MasterDataMixin, models.Model):
    """
    Eltartott minőség törzs
    """
    class Meta:
        db_table = 'dependent_qualities'
        verbose_name = _('eltartott minőség')
        verbose_name_plural = _('eltartott minőségek')

class DependentRight(MasterDataMixin, models.Model):
    """
    Eltartott jogosultság törzs
    """
    class Meta:
        db_table = 'dependent_rights'
        verbose_name = _('eltartott jogosultság')
        verbose_name_plural = _('eltartott jogosultságok')


class Tax(MasterDataMixin, models.Model):
    """
    Adónem törzs
    """
    class Meta:
        db_table = 'taxes'
        verbose_name = _("adónem")
        verbose_name_plural = _("adónemek")


class Discount(MasterDataMixin, models.Model):
    """
    Adó kedvezmény törzs
    """
    class Meta:
        db_table = 'discounts'
        verbose_name = _("adókedvezmény")
        verbose_name_plural = _("adókedvezmények")

    tax = models.ForeignKey(
        to=Tax,
        on_delete=models.CASCADE,
        verbose_name=_('adónem'),
        related_name='discounts',
        blank=False,
        null=False
    )

class Legal(MasterDataMixin, models.Model):
    """
    Jogviszony törzs
    """
    class Meta:
        db_table = 'legals'
        verbose_name = _("jogviszony")
        verbose_name_plural = _("jogviszonyok")

class PauseCategory(MasterDataMixin, models.Model):
    """
    Biztosítás szünetelése törzs
    """
    class Meta:
        db_table = 'category_pause'
        verbose_name = _("biztosítás szünetelése")
        verbose_name_plural = _("biztosítás szünetelések")



class PayrollMode(MasterDataMixin, models.Model):
    """
    Számfejtés módja törzs
    """
    class Meta:
        db_table = 'payroll_modes'
        verbose_name = _('számfejtés módja')
        verbose_name_plural = _('számfejtés módjai')


class Pretence(MasterDataMixin, models.Model):
    """
    Jogcím törzs
    """
    class Meta:
        db_table = 'pretences'
        verbose_name = _("jogcím")
        verbose_name_plural = _("jogcímek")

class RevenueBase(MasterDataMixin, models.Model):
    """
    Jövedelem alapja törzs
    """
    class Meta:
        db_table = 'revenue_bases'
        verbose_name = _('jövedelem alapja')
        verbose_name_plural = _('jövedelem alapok')


class RevenueType(MasterDataMixin, models.Model):
    """
    Jövedelem típusa törzs
    """
    class Meta:
        db_table = 'revenue_types'
        verbose_name = _('jövedelem típus')
        verbose_name_plural = _('jövedelem típusok')


class TimeSheetCategory(MasterDataMixin, models.Model):
    """
    Jelenlét törzs
    """
    class Meta:
        db_table = 'category_timesheet'
        verbose_name = _("jelenléti ív törzs")
        verbose_name_plural = _("jelenléti ív törzsek")

class Title(MasterDataMixin, models.Model):
    """
    Név előtag törzs
    """
    class Meta:
        db_table = 'titles'
        verbose_name = _('előtag')
        verbose_name_plural = _('előtagok')


class UniformBookingClassificationSystem(MasterDataMixin, models.Model):
    """
    FEOR törzs
    """
    class Meta:
        db_table = 'ubcs_codes'
        verbose_name = _('FEOR kód')
        verbose_name_plural = _('FEAOR kódok')

class PrimeMarriageStatement(MasterDataMixin, models.Model):
    """
    Első házasok nyilatkozat törzs
    """
    class Meta:
        db_table = 'prime_marriage_statement'
        verbose_name = _('első házasok nyilatkozat')
        verbose_name_plural = _('első házasok nyilatkozatok')

class FamilyTaxDiscountStatement(MasterDataMixin, models.Model):
    """
    Családi adókedvezmény nyilatkozat törzs
    """
    class Meta:
        db_table = 'family_tax_discount_statements'
        verbose_name = _('családi adókedvezmény nyilatkozat')
        verbose_name_plural = _('családi adókedvezmény nyilatkozatok')

class SimplifiedBurdenSharingContributionTaxLimit(MasterDataMixin, models.Model):
    """
    EKHO adózási limit törzs
    """
    class Meta:
        db_table = 'simplified_burden_sharing_contribution_tax_limits'
        verbose_name = _('EKHO adózási limit')
        verbose_name_plural = _('EKHO adózási limitek')

class Pause(IntervalMixin, models.Model):
    class Meta:
        db_table = 'pauses'
        verbose_name = _("biztosítás szünetelése")
        verbose_name_plural = _("biztosítás szünetelések")

    category = models.ForeignKey(
        verbose_name=_("kategória"),
        to=PauseCategory,
        related_name='categories',
        on_delete=models.CASCADE,
    )

class WorkDay(models.Model):
    class Meta:
        db_table = 'workdays'
        verbose_name = _("munkanap")
        verbose_name_plural = _("munkanapok")

class WorkSheet(models.Model):
    class Meta:
        db_table = 'worksheets'
        verbose_name = _("munkalap")
        verbose_name_plural = _("munkalapok")

