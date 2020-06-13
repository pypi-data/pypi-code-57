from django.db import models
from django.conf import settings
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import fields

from ..bakery.models import BuildableWagtailBakeryModel
from .. import constants
from ..amp.mixins import AmpMixin
from ...loader import get_model


GenericPage = get_model('cms', 'GenericPage')
Svg = get_model('cms', 'Svg')




import json
from django import forms
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from wagtail.admin.staticfiles import versioned_static
from wagtail.admin.widgets import AdminChooser
from wagtail.documents import get_document_model


class AdminSvgChooser(AdminChooser):
    choose_one_text = _('Choose a document')
    choose_another_text = _('Choose another document')
    link_to_chosen_text = _('Edit this document')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.document_model = Svg

    def render_html(self, name, value, attrs):
        instance, value = self.get_instance_and_id(self.document_model, value)
        original_field_html = super().render_html(name, value, attrs)

        return render_to_string("wagtaildocs/widgets/document_chooser.html", {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'document': instance,
        })

    def render_js_init(self, id_, name, value):
        return "createDocumentChooser({0});".format(json.dumps(id_))

    @property
    def media(self):
        return forms.Media(js=[
            versioned_static('wagtaildocs/js/document-chooser-modal.js'),
            versioned_static('wagtaildocs/js/document-chooser.js'),
        ])

from wagtail.admin.edit_handlers import BaseChooserPanel
class SvgChooserPanel(BaseChooserPanel):
    object_type_name = "svg"

    def widget_overrides(self):
        return {self.field_name: AdminSvgChooser}


class AHomePage(AmpMixin, BuildableWagtailBakeryModel, GenericPage):
    template = '%s/home_page.html' % constants.PAGES_TEMPLATES_PATH
    svg_bg_desktop = models.ForeignKey(
        Svg,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Search Block - Background Desktop Search Block",
        help_text="SVG",
    )
    svg_bg_mobile = models.ForeignKey(
        Svg,
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
                         SvgChooserPanel('svg_bg_desktop'),
                         SvgChooserPanel('svg_bg_mobile'),
                         FieldPanel('h1'),
                         FieldPanel('search_text'),
                         FieldPanel('search_placeholder'),
                     ] + GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'
