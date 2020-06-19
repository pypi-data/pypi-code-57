from django.db import models
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel

from webspace.loader import get_model


MyDocument = get_model('cms', 'MyDocument')


class AIconSnippet(index.Indexed, models.Model):
    key = models.CharField(max_length=255)
    light = models.ForeignKey(
        MyDocument,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    space = models.ForeignKey(
        MyDocument,
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

    @staticmethod
    def get_context():
        IconSnippet = get_model('cms', 'IconSnippet')
        ret = {}
        DEFAULT_LINK = '/static/webspace/img/svg/default.svg'
        for icon in IconSnippet.objects.all():
            ret[icon.key] = {
                'space': icon.space.url if icon.space else DEFAULT_LINK,
                'light': icon.light.url if icon.light else DEFAULT_LINK,
            }
        return ret

    class Meta:
        verbose_name = "Icon"
        abstract = True
        app_label = 'cms'
