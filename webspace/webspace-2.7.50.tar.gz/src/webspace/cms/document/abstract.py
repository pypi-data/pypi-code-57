from wagtail.documents.models import Document, AbstractDocument
from django.db import models


class AMyDocument(AbstractDocument):
    #  Dimensions for SVG

    width = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        help_text="for SVG"
    )
    height = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        help_text="for SVG"
    )

    admin_form_fields = Document.admin_form_fields + (
        'width',
        'height'
    )

    def get_size(self):
        return '500x500'

    class Meta:
        app_label = 'cms'
        abstract = True
