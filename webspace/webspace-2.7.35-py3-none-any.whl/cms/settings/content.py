from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList


@register_setting
class AContentSettings(BaseSetting):
    logo = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    brand_tab_panels = [
        ImageChooserPanel('logo'),
    ]

    organization_panels = [
    ]

    edit_handler = TabbedInterface([
        ObjectList(brand_tab_panels, heading='Brand'),
        ObjectList(organization_panels, heading='Organization'),
    ])

    class Meta:
        verbose_name = 'Content'
        abstract = True
        app_label = 'cms'
