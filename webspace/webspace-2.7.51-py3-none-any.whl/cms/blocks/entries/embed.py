from webspace.cms import constants
from webspace.cms.blocks.common import EntryBlock, EmbedWithSizeBlock


class EmbedEntry(EntryBlock):
    amp_scripts = ['iframe']
    embed = EmbedWithSizeBlock()

    def mock(self, size_media='m', *args, **kwargs):
        self.mock_data.update({
            'type': 'embed',
            'value': {
                'embed': {
                    "link": self.mocker.URL_EMBED,
                    'size': size_media
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/embed.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Embed"
