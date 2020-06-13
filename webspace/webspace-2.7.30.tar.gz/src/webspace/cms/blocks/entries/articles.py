from wagtail.core import blocks

from ... import constants
from ..common import BaseBlock


class Articles(BaseBlock):
    articles = blocks.StreamBlock(
        [
            ('article', blocks.PageChooserBlock(required=False, target_model='cms.BlogPage')),
        ],
        min_num=1
    )

    class Meta:
        template = '%s/entries/articles.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Articles"
