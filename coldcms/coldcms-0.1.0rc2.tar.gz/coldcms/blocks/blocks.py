from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks


class LinkStructValue(blocks.StructValue):
    def url(self):
        if self.get("custom_url"):
            return self.get("custom_url") + self.get("extra_url", "")
        elif self.get("page"):
            return self.get("page").url + self.get("extra_url", "")
        return self.get("extra_url") or "#"

    def text(self):
        if self.get("text"):
            return self.get("text")
        if self.get("page"):
            return self.get("page").title
        return self.url()


class CTABlock(blocks.StructBlock):
    text = blocks.CharBlock(
        label=_("Link text"),
        help_text=_(
            "Use this as the text of an external URL or if you want to "
            "override the Page's title"
        ),
        required=False,
        max_length=40,
    )
    custom_url = blocks.CharBlock(label=_("External URL"), required=False)
    page = blocks.PageChooserBlock(
        label=_("Link to an internal page"),
        help_text=_("Ignored if the external URL is used"),
        required=False,
    )
    extra_url = blocks.CharBlock(
        label=_("Append to URL"),
        help_text=_("Use this to optionally append a #hash or querystring to the URL."),
        required=False,
        default="",
    )

    class Meta:
        icon = "site"
        value_class = LinkStructValue
