from wagtail.core import blocks

from ... import constants
from ..common import SvgWithSizeBlock, ImageWithSizeBlock, BaseBlock, TextBlock, ButtonBlock
from ..choice import AlignTextChoiceBlock


class MediaText(BaseBlock):
    h2 = blocks.CharBlock()
    text = TextBlock()
    media = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
        ],
        max_num=1
    )
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=2
    )
    reverse = blocks.BooleanBlock(required=False)
    section = blocks.BooleanBlock(required=False)
    align = AlignTextChoiceBlock(required=False)

    class Meta:
        template = '%s/entries/media_text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Media Text"
