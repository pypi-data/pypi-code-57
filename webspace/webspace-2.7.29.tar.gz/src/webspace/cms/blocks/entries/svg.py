from ... import constants
from ..common import SvgWithSizeBlock, BaseBlock


class Svg(BaseBlock):
    svg = SvgWithSizeBlock()

    class Meta:
        template = '%s/entries/svg.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Svg"
        icon = 'image'
