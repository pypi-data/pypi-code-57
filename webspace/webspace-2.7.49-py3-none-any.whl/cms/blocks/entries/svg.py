from webspace.cms import constants
from webspace.cms.blocks.common import \
    EntryBlock, \
    SvgWithSizeBlock


class SvgEntry(EntryBlock):
    svg = SvgWithSizeBlock()

    def mock(self, force_file=None, size='m', *args, **kwargs):
        if 'theme' in kwargs:
            file = self.mocker.SVG_CONTENT_WIDTH_LIGHT \
                if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.SVG_CONTENT_WIDTH_SPACE
        else:
            file = self.mocker.SVG_CONTENT_WIDTH_LIGHT
        self.mock_data.update({
            'type': 'svg',
            'value': {
                'svg': {
                    'file': self.mocker.file(file if not force_file else force_file).id,
                    'size': size
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/svg.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Svg"
        icon = 'image'
