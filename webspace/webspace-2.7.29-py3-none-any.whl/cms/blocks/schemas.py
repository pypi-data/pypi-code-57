from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .. import constants


class HowToStep(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    image = ImageChooserBlock(label="Image 500x500", required=False)
    name = blocks.CharBlock(required=True)
    url = blocks.URLBlock(required=False)


class HowTo(blocks.StructBlock):
    name = blocks.CharBlock(required=True)
    description = blocks.CharBlock(required=True)
    image = ImageChooserBlock(label="Image 500x500", required=True)
    step = blocks.StreamBlock(
        [
            ('step', HowToStep()),
        ],
    )

    class Meta:
        label = "Schema HowTo"
        template = '%s/schemas/how_to.html' % constants.BLOCK_TEMPLATES_PATH


class Question(blocks.StructBlock):
    question = blocks.CharBlock(required=True)
    answer = blocks.CharBlock(required=True)


class FAQPage(blocks.StructBlock):
    questions = blocks.StreamBlock(
        [
            ('questions', Question()),
        ],
    )

    class Meta:
        label = "Schema FAQPage"
        template = '%s/schemas/faq_page.html' % constants.BLOCK_TEMPLATES_PATH
