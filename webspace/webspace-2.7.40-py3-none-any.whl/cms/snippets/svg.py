from django.db import models
from wagtail.documents.models import Document, AbstractDocument


class ASvg(AbstractDocument):
    ratio = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Example 4/3'
    )

    admin_form_fields = Document.admin_form_fields + (
        'ratio',
    )

    class Meta:
        verbose_name = "Svg"
        abstract = True
        app_label = 'cms'
