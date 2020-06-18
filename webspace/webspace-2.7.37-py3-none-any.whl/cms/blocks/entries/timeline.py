from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    EntryBlock


class TimeLineEntry(EntryBlock):
    items = blocks.StreamBlock(
        [
            ('text', TextBlock()),
        ],
        min_num=1
    )

    def mock(self, *args, **kwargs):
        item = {
            'type': 'text',
            'value': {
                'value': self.mocker.xs
            }
        }
        self.mock_data.update({
            'type': 'timeline',
            'value': {
                'items': [
                    item,
                    item,
                    item,
                    item,
                    item
                ]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/timeline.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Timeline"
