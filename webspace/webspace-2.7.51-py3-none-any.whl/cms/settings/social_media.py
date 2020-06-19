from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class ASocialMediaSettings(BaseSetting):
    facebook = models.URLField(help_text='Facebook page URL')
    instagram = models.URLField(help_text='Instagram page URL')
    linkedin = models.URLField(help_text='Linkedin page URL')

    class Meta:
        verbose_name = 'Social media'
        abstract = True
        app_label = 'cms'
