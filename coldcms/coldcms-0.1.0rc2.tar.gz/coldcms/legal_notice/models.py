from coldcms.wagtail_customization.mixins import ColdCMSPageMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class LegalNoticePage(ColdCMSPageMixin, Page):
    """Legal Notice model."""

    subtitle = models.TextField(blank=True, null=True, verbose_name=_("Subtitle"))
    content = RichTextField(verbose_name=_("Content"))

    template = "legal_notice/legal_notice.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    parent_page_types = []
    content_panels = Page.content_panels + [FieldPanel("content")]

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
        verbose_name = _("Legal notice")
