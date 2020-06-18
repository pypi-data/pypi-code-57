from wagtail.core.blocks import StaticBlock
from ... import constants


class Calendly(StaticBlock):
    class Meta:
        template = '%s/static/calendly.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Calendly"
