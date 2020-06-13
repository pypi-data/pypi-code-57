from wagtail.admin.edit_handlers import StreamFieldPanel

from ..amp.mixins import AmpMixin
from ..bakery.models import BuildableWagtailBakeryModel
from .. import constants

from ...loader import get_model

GenericPage = get_model('cms', 'GenericPage')


class AContentPage(AmpMixin, BuildableWagtailBakeryModel, GenericPage):
    template = '%s/content_page.html' % constants.PAGES_TEMPLATES_PATH

    promote_panels = GenericPage.promote_panels + [
        StreamFieldPanel('schemas'),
    ]

    class Meta:
        abstract = True
        app_label = 'cms'
