from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class PartnerBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=70, label=_("Name"))
    website_url = blocks.CharBlock(label=_("Partener's Website"))
    logo = ImageChooserBlock()

    class Meta:
        icon = "group"


class PartnerCategoryBlock(blocks.StructBlock):
    category_name = blocks.CharBlock(
        max_length=70,
        label=_("Category name"),
        help_text=_("The category of partner (ex: Institution)"),
        required=False,
    )
    partners = blocks.StreamBlock([("partners", PartnerBlock())], label=_("Partners"))

    class Meta:
        label = _("Partners' group")
        icon = "group"


class PartnersPage(ColdCMSPageMixin, Page):
    """Partners model."""

    content = RichTextField(blank=True, default="", verbose_name=_("Content"))
    partners_groups = StreamField(
        [("partners_groups", PartnerCategoryBlock())],
        blank=True,
        null=True,
        verbose_name=_("Partners' groups"),
    )

    template = "partners/partners.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("content"),
        StreamFieldPanel("partners_groups"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(
                [MultiFieldPanel([FieldPanel("show_in_menus")])],
                heading=_("Settings"),
                classname="settings",
            ),
        ]
    )

    class Meta:
        verbose_name = _("Partners")
