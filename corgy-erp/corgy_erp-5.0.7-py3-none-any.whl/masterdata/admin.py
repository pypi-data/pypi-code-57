from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.ApplianceQuality)
class ApplianceQualityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AutonomeActivityStatement)
class AutonomeActivityStatementAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusinessForm)
class BusinessFormAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Contribution)
class ContributionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.DependentQuality)
class DependentQualityAdmin(admin.ModelAdmin):
    pass

@admin.register(models.DependentRight)
class DependentRightAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FamilyTaxDiscountStatement)
class FamilyTaxDiscountStatementAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Legal)
class LegalAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PauseCategory)
class PauseCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.PayrollMode)
class PayrollModeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Pretence)
class PretenceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RevenueBase)
class RevenueBaseAdmin(admin.ModelAdmin):
    pass

@admin.register(models.RevenueType)
class RevenueTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Tax)
class TaxAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TimeSheetCategory)
class TimeSheetCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    pass

@admin.register(models.UniformBookingClassificationSystem)
class UniformBookingClassificationSystemAdmin(admin.ModelAdmin):
    pass
