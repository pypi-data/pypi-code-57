from wagtail.core import blocks

from ... import constants
from ..common import SvgBlock, ImageBlock, BaseBlock


class SvgLabel(SvgBlock):
    label = blocks.CharBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)


class ImageLabel(ImageBlock):
    label = blocks.CharBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)


class MediasLine(BaseBlock):
    medias = blocks.StreamBlock(
        [
            ('svg_label', SvgLabel()),
            ('image_label', ImageLabel()),
        ],
        min_num=1
    )

    class Meta:
        template = '%s/entries/medias_line.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Medias Line"
