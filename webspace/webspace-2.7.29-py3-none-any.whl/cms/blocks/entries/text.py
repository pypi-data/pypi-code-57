from ... import constants
from ..common import BaseBlock, TextBlock
from ..choice import AlignTextChoiceBlock


class Text(BaseBlock):
    text = TextBlock()
    align = AlignTextChoiceBlock(required=False)

    class Meta:
        template = '%s/entries/text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Text"
        icon = 'edit'
