from wagtail.core import blocks
from webspace.cms.blocks.common import EntryBlock
from webspace.cms import constants


class CalendlyEntry(EntryBlock):
    link = blocks.URLBlock(required=False)

    class Meta:
        template = '%s/entries/calendly.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Calendly"

    def mock(self, *args, **kwargs):
        self.mock_data.update({
            'type': 'calendly',
            'value': {
                'link': "https://calendly.com/station-spatiale/30min?hide_event_type_details=1&background_color=20202C&text_color=F7F7F7&primary_color=2FB196"
            }
        })
        return super().mock(*args, **kwargs)
