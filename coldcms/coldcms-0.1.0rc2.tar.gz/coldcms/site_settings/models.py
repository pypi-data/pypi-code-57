from coldcms.blocks.blocks import CTABlock
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting(icon="code")
class Footer(BaseSetting, ClusterableModel):
    """A footer containing a list of footer columns"""

    panels = [InlinePanel("columns", label=_("Footer columns"))]

    def __str__(self):
        return "Footer"

    class Meta:
        verbose_name_plural = _("Footer")
        verbose_name = _("Footer")


class FooterColumn(Orderable):
    footer = ParentalKey("site_settings.Footer", related_name="columns")
    title = models.CharField(
        max_length=40, verbose_name=_("Title"), blank=True, null=True
    )
    links = StreamField(
        [("links", CTABlock(icon="link"))],
        blank=True,
        null=True,
        verbose_name=_("Links"),
    )

    panels = [FieldPanel("title"), StreamFieldPanel("links")]


@register_setting(icon="image")
class SiteSettings(BaseSetting):
    """Site settings"""

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Logo"),
    )

    panels = [ImageChooserPanel("logo")]

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logos")


@register_setting(icon="doc-full-inverse")
class CSSStyleSheet(BaseSetting):
    """Load a CSS stylesheet"""

    CSS_stylesheet = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        help_text=_(
            "Upload your own CSS stylesheet to custom the appearance of your website"
        ),
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("CSS"),
    )

    panels = [DocumentChooserPanel("CSS_stylesheet")]

    class Meta:
        verbose_name = _("CSS stylesheet")
        verbose_name_plural = _("CSS stylesheets")


@register_setting(icon="collapse-down")
class MenuOptions(BaseSetting):
    """Option to show or hide the menu bar"""

    hide_menu = models.BooleanField(
        verbose_name=_("Hide Menu"),
        default=False,
        help_text=_("Whether to hide the menu bar or not"),
    )

    panels = [FieldPanel("hide_menu")]

    class Meta:
        verbose_name = _("Menu options")
