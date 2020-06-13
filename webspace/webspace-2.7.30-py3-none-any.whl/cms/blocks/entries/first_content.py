from wagtail.core import blocks

from ... import constants
from ..common import BaseBlock, TextBlock, ButtonBlock
from ..choice import AlignTextChoiceBlock


class FirstContent(BaseBlock):
    h1 = blocks.CharBlock()
    text = TextBlock()
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=2,
        required=False
    )
    align = AlignTextChoiceBlock(required=False)

    class Meta:
        template = '%s/entries/first_content.html' % constants.BLOCK_TEMPLATES_PATH
        label = "First Content"
