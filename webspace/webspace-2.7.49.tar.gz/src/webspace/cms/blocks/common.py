import re
from django.utils.text import slugify
from django.conf import settings
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.rich_text import RichText
from wagtail.core import blocks

from webspace.cms.blocks.mocker import Mocker
from webspace.cms import constants
from webspace.cms.amp.utils import amp_mode_active
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
    size = SizeChoiceBlock(required=False)

    class Meta:
        template = '%s/common/svg.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Svg"


class ImageBlock(blocks.StructBlock):
    file = ImageChooserBlock(label="Image 500x500", required=False)


class ImageWithSizeBlock(ImageBlock):
    size = SizeChoiceBlock(required=False)

    class Meta:
        template = '%s/common/image.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Image"


class EmbedBlock(blocks.StructBlock):
    link = blocks.URLBlock(required=False)


class EmbedWithSizeBlock(EmbedBlock):
    size = SizeChoiceBlock(required=False)

    class Meta:
        template = '%s/common/embed.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Embed"


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



class EntryBlock(blocks.StructBlock):
    bg_desktop = blocks.StreamBlock(
        [
            ('image', ImageChooserBlock()),
            ('svg', DocumentChooserBlock()),
        ],
        max_num=1,
        required=False
    )
    bg_mobile = blocks.StreamBlock(
        [
            ('image', ImageChooserBlock()),
            ('svg', DocumentChooserBlock()),
        ],
        max_num=1,
        required=False
    )
    svg_bg_position = BackgroundPositionChoiceBlock(
        required=False,
        default=constants.BACKROUND_POSITION_CENTER
    )
    theme = ThemeChoiceBlock(required=False)
    container = ContainerChoiceBlock(required=False)
    padding_top = blocks.BooleanBlock(default=True, required=False)
    padding_bottom = blocks.BooleanBlock(default=True, required=False)

    def __init__(self):
        super().__init__()
        self.mock_data = {}
        self.mocker = Mocker()
        self.random_counter = 0

    def mock(self, bg=False, padding=True, container='regular', theme=constants.THEME_SPACE):
        if bg:
            bg_desktop = self.mocker.SVG_BG_DESKTOP_LIGHT if theme == constants.THEME_LIGHT else self.mocker.SVG_BG_DESKTOP_SPACE
            bg_mobile = self.mocker.SVG_BG_MOBILE_LIGHT if theme == constants.THEME_LIGHT else self.mocker.SVG_BG_MOBILE_SPACE
            self.mock_data['value'].update({
                'bg_desktop': [{
                    'type': 'svg',
                    'value': self.mocker.file(bg_desktop).id if bg else None
                }],
                'bg_mobile': [{
                    'type': 'svg',
                    'value': self.mocker.file(bg_mobile).id if bg else None
                }]
            })
        self.mock_data['value'].update({
            'theme': theme,
            'container': container,
            'padding': padding
        })
        copy = self.mock_data.copy()
        self.mock_data = {}
        self.random_counter += 1
        return copy

    def get_template(self, context=None):
        if amp_mode_active():
            return self.meta.template.replace('.html', '_amp.html')
        return self.meta.template
