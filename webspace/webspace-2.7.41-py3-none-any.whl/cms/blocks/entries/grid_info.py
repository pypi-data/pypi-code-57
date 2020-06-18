from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    SvgBlock, \
    ImageBlock, \
    EntryBlock


class SvgInfo(SvgBlock):
    title = blocks.CharBlock()
    text_hover = TextBlock()


class ImageInfo(ImageBlock):
    title = blocks.CharBlock()
    text_hover = TextBlock()


class GridInfoEntry(EntryBlock):
    infos = blocks.StreamBlock(
        [
            ('svg_info', SvgInfo()),
            ('image_info', ImageInfo()),
        ],
        min_num=1
    )

    def mock(self, *args, **kwargs):
        if 'theme' in kwargs:
            file = self.mocker.SVG_ICON_LIGHT \
                if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.SVG_ICON_SPACE
        else:
            file = self.mocker.SVG_ICON_SPACE
        info = {
            'type': 'svg_info',
            'value': {
                'file': self.mocker.file(file).id,
                'title': "Lorem ipsum",
                'text_hover': {
                    'value': "<h3>lorem ipsum dolor sit amet consectetur adipisicing elit sed do eiusmod</h3>"
                }
            }
        }
        self.mock_data.update({
            'type': 'grid_info',
            'value': {
                'infos': [
                    info,
                    info,
                    info,
                    info,
                    info,
                    info,
                ]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/grid_info.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Grid Info"
