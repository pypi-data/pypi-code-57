from django.db import models
from django.conf import settings
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import fields
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from ..bakery.models import BuildableWagtailBakeryModel
from .. import constants
from ..amp.mixins import AmpMixin
from ...loader import get_model


GenericPage = get_model('cms', 'GenericPage')


class AHomePage(AmpMixin, BuildableWagtailBakeryModel, GenericPage):
    template = '%s/home_page.html' % constants.PAGES_TEMPLATES_PATH
    svg_bg_desktop = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Search Block - Background Desktop Search Block",
        help_text="SVG",
    )
    svg_bg_mobile = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Search Block - Background Mobile",
        help_text="SVG",
    )
    h1 = models.CharField(
        default='',
        max_length=200,
        blank=True,
        verbose_name="Search Block - H1",
    )
    search_text = fields.RichTextField(
        default='',
        blank=True,
        features=settings.RICH_TEXT_FEATURES,
        verbose_name="Search Block - Text",
    )
    search_placeholder = models.CharField(
        default='',
        max_length=200,
        blank=True,
        verbose_name="Search Block - Placeholder",
    )

    content_panels = [
                         DocumentChooserPanel('svg_bg_desktop'),
                         DocumentChooserPanel('svg_bg_mobile'),
                         FieldPanel('h1'),
                         FieldPanel('search_text'),
                         FieldPanel('search_placeholder'),
                     ] + GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'
