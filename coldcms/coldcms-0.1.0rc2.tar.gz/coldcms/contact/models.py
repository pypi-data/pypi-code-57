from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.db import models
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


class OpeningHour(blocks.StructBlock):
    day = blocks.CharBlock(help_text=_("example: Monday"), label=_("Day of the week"),)
    hours = blocks.CharBlock(
        help_text=_("example: 10h-12h ; 14h-20h"),
        label=_("Opening hours for the given day"),
    )


class ContactPage(ColdCMSPageMixin, Page):
    """Contact model."""

    content = RichTextField(blank=True, default="", verbose_name=_("Content"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    phone_number = models.CharField(
        blank=True, null=True, max_length=20, verbose_name=_("Phone number")
    )
    email = models.EmailField(verbose_name=_("Contact email"), blank=True, null=True)
    opening_hours = StreamField(
        [("opening_hours", OpeningHour(icon="time"))],
        blank=True,
        null=True,
        verbose_name=_("Opening hours"),
    )
    opening_hours_free_text = RichTextField(
        verbose_name=_("Opening hours exception or precisions"),
        help_text=_("Put here exceptions like vacation, Bank holidays and so on..."),
        blank=True,
        null=True,
        features=["bold", "italic", "link", "document-link", "ol", "ul", "hr"],
    )

    template = "contact/contact.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("content"),
        FieldPanel("address"),
        FieldPanel("phone_number"),
        FieldPanel("email"),
        StreamFieldPanel("opening_hours"),
        FieldPanel("opening_hours_free_text"),
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
        verbose_name = _("Contact Page")
