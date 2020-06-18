from wagtail.admin.edit_handlers import StreamFieldPanel

from webspace.cms.amp.mixins import AmpMixin
from webspace.cms.bakery.abstract import WagtailPageBakeryModel
from webspace.cms import constants
from webspace.loader import get_model

GenericPage = get_model('cms', 'GenericPage')


class AContentPage(AmpMixin, WagtailPageBakeryModel, GenericPage):
    template = '%s/content_page.html' % constants.PAGES_TEMPLATES_PATH

    promote_panels = GenericPage.promote_panels + [
        StreamFieldPanel('schemas'),
    ]

    class Meta:
        abstract = True
        app_label = 'cms'
