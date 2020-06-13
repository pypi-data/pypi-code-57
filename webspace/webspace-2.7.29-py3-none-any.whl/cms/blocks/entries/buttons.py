from wagtail.core import blocks

from ... import constants
from ..choice import AlignTextChoiceBlock
from ..common import ButtonBlock, BaseBlock


class Buttons(BaseBlock):
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=3
    )
    align = AlignTextChoiceBlock(required=False)

    class Meta:
        template = '%s/entries/buttons.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Buttons"
