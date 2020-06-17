from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin


class WidgetConfig(CMSPlugin):
    reference = models.CharField(_("Reference"), max_length=255, help_text=_("OpenSystem reference (e.g.: CVERT-90333)"))

    def __unicode__(self):
        return self.reference
