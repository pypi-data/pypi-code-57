from wagtail.core import blocks
from ... import constants
from ..common import BaseBlock, TextBlock


class TimeLine(BaseBlock):
    items = blocks.StreamBlock(
        [
            ('text', TextBlock()),
        ],
        min_num=1
    )

    class Meta:
        template = '%s/entries/timeline.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Timeline"
