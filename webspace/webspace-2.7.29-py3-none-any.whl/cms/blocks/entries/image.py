from wagtail.core import blocks

from ... import constants
from ..common import ImageWithSizeBlock, BaseBlock


class Image(BaseBlock):
    image = ImageWithSizeBlock()
    size_auto = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        template = '%s/entries/image.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Image"
        icon = 'image'
