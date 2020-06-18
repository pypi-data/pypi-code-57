from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.models import Image


@register_setting
class DataTypesSettings(BaseSetting):
    logo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    class Meta:
        verbose_name = 'Data Types'
