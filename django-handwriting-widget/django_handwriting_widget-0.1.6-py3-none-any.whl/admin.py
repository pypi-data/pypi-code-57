from django.contrib.admin import ModelAdmin
from django.db.models import ImageField

from .forms import HandwritingPad


__all__ = [
    'HandwritingPadAdminMixin', 'HandwritingPadModelAdmin',
]


class HandwritingPadAdminMixin:
    formfield_overrides = {
        ImageField: {'widget': HandwritingPad},
    }


class HandwritingPadModelAdmin(HandwritingPadAdminMixin, ModelAdmin):
    pass
