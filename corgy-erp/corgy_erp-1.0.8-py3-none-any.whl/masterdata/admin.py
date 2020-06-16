from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from .models import BusinessForm
from .models import Contribution
from .models import Discount
from .models import PauseCategory
from .models import Pretence
from .models import Tax
from .models import TimeSheetCategory
from .models import Legal

@admin.register(BusinessForm)
class BusinessFormAdmin(admin.ModelAdmin):
    pass


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(PauseCategory)
class PauseCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Pretence)
class PretenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    pass

@admin.register(TimeSheetCategory)
class TimeSheetCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Legal)
class LegalAdmin(admin.ModelAdmin):
    pass
