from django.contrib import admin
from happy_quotas.models import Quota


@admin.register(Quota)
class QuotaAddmin(admin.ModelAdmin):
    pass
