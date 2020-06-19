from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    InlinePanel,
    FieldPanel,
    PageChooserPanel,
)
from wagtail.core.models import Orderable


class AMenuItem(Orderable):
    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)
    menu = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'

    class Meta:
        verbose_name = "Icon"
        abstract = True
        app_label = 'cms'


class AMenu(ClusterableModel):
    help_text = models.CharField(max_length=100, default='', blank=True)
    title = models.CharField(max_length=100)

    panels = [
        MultiFieldPanel([
            FieldPanel("help_text"),
            FieldPanel("title"),
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Items")
    ]

    def __str__(self):
        return self.help_text

    class Meta:
        abstract = True
        app_label = 'cms'
