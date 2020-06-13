from wagtail.core import blocks

from ... import constants
from ..common import SvgBlock, ImageBlock, BaseBlock, TextBlock


class SvgInfo(SvgBlock):
    title = blocks.CharBlock()
    text_hover = TextBlock()


class ImageInfo(ImageBlock):
    title = blocks.CharBlock()
    text_hover = TextBlock()


class GridInfo(BaseBlock):
    infos = blocks.StreamBlock(
        [
            ('svg_info', SvgInfo()),
            ('image_info', ImageInfo()),
        ],
        min_num=1
    )

    class Meta:
        template = '%s/entries/grid_info.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Grid Info"
