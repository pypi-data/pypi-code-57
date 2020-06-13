from wagtail.core import blocks
from ... import constants
from ..common import BaseBlock, SvgWithSizeBlock, TextBlock, ButtonBlock


class CustomCard(blocks.StructBlock):
    svg = SvgWithSizeBlock()
    text = TextBlock()
    button = ButtonBlock()

    class Meta:
        template = '%s/common/custom_card.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Custom Card"


class Cards(BaseBlock):
    amp_scripts = ['carousel']
    cards = blocks.StreamBlock(
        [
            ('custom', CustomCard()),
        ],
        min_num=1
    )
    carousel = blocks.BooleanBlock(required=False)
    carousel_cta = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        template = '%s/entries/cards.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Cards"
        #  icon = 'image'
