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


class QuestionBlock(blocks.StructBlock):
    question = blocks.CharBlock(max_length=255, label=_("Question"))
    answer = blocks.RichTextBlock(
        features=["bold", "italic", "link", "document-link", "ol", "ul", "hr"],
        label=_("Answer"),
    )

    class Meta:
        icon = "help"


class QuestionCategoryBlock(blocks.StructBlock):
    category_name = blocks.CharBlock(
        max_length=70,
        help_text=_(
            "The type of question (ex: Accessibility, Rules). You can "
            "keep this field empty if you only have one category of "
            "questions/answers"
        ),
        required=False,
        label=_("Category name"),
    )
    questions = blocks.StreamBlock(
        [("questions", QuestionBlock())], label=_("Questions")
    )

    class Meta:
        icon = "help"
        label = _("Question group")


class FAQPage(ColdCMSPageMixin, Page):
    """FAQ model."""

    content = RichTextField(blank=True, default="", verbose_name=_("Content"))
    questions_groups = StreamField(
        [("questions_groups", QuestionCategoryBlock())],
        blank=True,
        null=True,
        verbose_name=_("Question groups"),
    )

    template = "faq/faq.html"
    show_in_menus_default = True
    search_fields = []
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("content"),
        StreamFieldPanel("questions_groups"),
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
        verbose_name = _("FAQ Page")
