import re
from django.utils.text import slugify
from django.conf import settings
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.rich_text import RichText
from wagtail.core import blocks

from .. import constants
from ..amp.utils import amp_mode_active

from .choice import \
    ThemeChoiceBlock, \
    SizeChoiceBlock, \
    ContainerChoiceBlock, \
    ButtonChoiceBlock, \
    BackgroundPositionChoiceBlock

#  Add ids to headlines
__original__html__ = RichText.__html__
heading_re = r"<h(\d)[^>]*>([^<]*)</h\1>"


def add_id_attribute(match):
    n = match.group(1)
    text_content = match.group(2)
    id = slugify(text_content)
    return f'<h{n} id="{id}">{text_content}</h{n}>'


def with_heading_ids(self):
    html = __original__html__(self)
    return re.sub(heading_re, add_id_attribute, html)


RichText.__html__ = with_heading_ids


class TextBlock(blocks.StructBlock):
    value = blocks.RichTextBlock(required=False, features=settings.RICH_TEXT_FEATURES)

    class Meta:
        template = '%s/common/text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Text"


class SvgBlock(blocks.StructBlock):
    file = DocumentChooserBlock(required=False)


class SvgWithSizeBlock(SvgBlock):
    size = SizeChoiceBlock()

    class Meta:
        template = '%s/common/svg.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Svg"


class ImageBlock(blocks.StructBlock):
    file = ImageChooserBlock(label="Image 500x500", required=False)


class ImageWithSizeBlock(ImageBlock):
    size = SizeChoiceBlock()

    class Meta:
        template = '%s/common/image.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Image"


class BackgroundBlock(blocks.StructBlock):
    desktop = SvgBlock()
    mobile = SvgBlock()


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    link = blocks.URLBlock(required=False)
    page = blocks.PageChooserBlock(required=False)
    open_new_tab = blocks.BooleanBlock(default=False, required=False)
    type = ButtonChoiceBlock()

    class Meta:
        template = '%s/common/button.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Button"


class AMPStructBlock(blocks.StructBlock):

    def get_template(self, context):
        if amp_mode_active():
            return self.meta.template.replace('.html', '_amp.html')
        return self.meta.template


class BaseBlock(AMPStructBlock):
    svg_bg = BackgroundBlock(required=False)
    svg_bg_position = BackgroundPositionChoiceBlock(required=False)
    theme = ThemeChoiceBlock(required=False)
    container = ContainerChoiceBlock(required=False)
    padding_top = blocks.BooleanBlock(default=True, required=False)
    padding_bottom = blocks.BooleanBlock(default=True, required=False)
