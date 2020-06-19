from wagtail.core.blocks import StaticBlock

from webspace.cms import constants


class SocialShare(StaticBlock):
    class Meta:
        template = '%s/static/social_share.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Social Share"

    def mock(self):
        return {
            'type': 'social_share'
        }
