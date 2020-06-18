from webspace.cms.bakery.abstract import WagtailPageBakeryModel
from webspace.cms import constants
from webspace.cms.amp.mixins import AmpMixin
from webspace.loader import get_model


GenericPage = get_model('cms', 'GenericPage')


class AHomePage(AmpMixin, WagtailPageBakeryModel, GenericPage):
    template = '%s/home_page.html' % constants.PAGES_TEMPLATES_PATH
    content_panels = GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'
