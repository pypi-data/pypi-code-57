from wagtail.core import blocks

from ... import constants
from ..common import BaseBlock


class Embed(BaseBlock):
    amp_scripts = ['iframe']
    link = blocks.URLBlock(required=False)

    class Meta:
        template = '%s/entries/embed.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Embed"
