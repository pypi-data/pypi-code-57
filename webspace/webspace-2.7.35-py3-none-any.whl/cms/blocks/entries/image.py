from wagtail.core import blocks
from wagtail.images.models import Image
from webspace.cms import constants
from webspace.cms.blocks.common import ImageWithSizeBlock, EntryBlock


class ImageEntry(EntryBlock):
    image = ImageWithSizeBlock()

    def mock(self, force_file=None, size='m', *args, **kwargs):
        if 'theme' in kwargs:
            img = self.mocker.IMG_CONTENT_WIDTH_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.IMG_CONTENT_WIDTH_SPACE
        else:
            img = self.mocker.IMG_CONTENT_HEIGHT_SPACE
        self.mock_data.update({
            'type': 'image',
            'value': {
                'image': {
                    'file': self.mocker.file(img if not force_file else force_file).id,
                    'size': size
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/image.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Image"
        icon = 'image'
