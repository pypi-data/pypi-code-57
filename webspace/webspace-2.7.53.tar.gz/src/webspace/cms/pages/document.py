from urllib.request import urlopen

from django.db import models
from django.http import Http404
from django.http import HttpResponse

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from webspace.loader import get_model

MyDocument = get_model('cms', 'MyDocument')


class ADocumentPage(Page):
    document = models.ForeignKey(
        MyDocument,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        DocumentChooserPanel('document'),
    ]
    subpage_types = []

    def serve(self, request, *args, **kwargs):
        try:
            ct = 'application/pdf' if self.document.file_extension == 'pdf' else 'application/octet-stream'
            response = HttpResponse(urlopen(self.document.url).read(), content_type=ct)
            response['Content-Disposition'] = 'filename="' + self.document.filename
            return response
        except Exception:
            raise Http404("")

    class Meta:
        abstract = True
        app_label = 'cms'
