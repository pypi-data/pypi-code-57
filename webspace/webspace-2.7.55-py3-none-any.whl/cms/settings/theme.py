from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.admin.edit_handlers import FieldPanel


@register_setting
class AThemeSettings(BaseSetting):

    primary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    secondary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    tertiary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    quaternary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    quinary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")

    light_primary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    light_seconday = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    light_tertiary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")
    light_quaternary = models.CharField(default='', max_length=8, help_text="Couleur Hexa '#FFFFFF'")

    h1 = models.IntegerField(null=True, default=None)
    h2 = models.IntegerField(null=True, default=None)
    h3 = models.IntegerField(null=True, default=None)
    h4 = models.IntegerField(null=True, default=None)
    h5 = models.IntegerField(null=True, default=None)
    h6 = models.IntegerField(null=True, default=None)
    p = models.IntegerField(null=True, default=None)

    color_tab_panels = [
        FieldPanel('primary'),
        FieldPanel('secondary'),
        FieldPanel('tertiary'),
        FieldPanel('quaternary'),

        FieldPanel('light_primary'),
        FieldPanel('light_seconday'),
        FieldPanel('light_tertiary'),
        FieldPanel('light_quaternary'),

    ]
    font_tab_panels = [
        FieldPanel('h1'),
        FieldPanel('h2'),
        FieldPanel('h3'),
        FieldPanel('h4'),
        FieldPanel('h5'),
        FieldPanel('h1'),
        FieldPanel('h6'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(color_tab_panels, heading='Colors'),
        ObjectList(font_tab_panels, heading='Typo'),
    ])

    class Meta:
        verbose_name = 'Theme'
        abstract = True
        app_label = 'cms'
