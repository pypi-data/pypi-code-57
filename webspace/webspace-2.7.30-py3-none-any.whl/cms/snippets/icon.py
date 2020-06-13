from django.db import models
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel


class AIconSnippet(index.Indexed, models.Model):
    key = models.CharField(max_length=255)
    light = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    space = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('key'),
        DocumentChooserPanel('light'),
        DocumentChooserPanel('space'),
    ]

    search_fields = [
        index.SearchField('key', partial_match=True),
    ]

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Icon"
        abstract = True
        app_label = 'cms'
