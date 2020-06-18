from wagtail.core import blocks

from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    SvgWithSizeBlock, \
    ImageWithSizeBlock, \
    ButtonBlock, \
    EntryBlock, \
    EmbedWithSizeBlock


class MediaTextEntry(EntryBlock):
    amp_scripts = ['iframe']
    h2 = blocks.CharBlock()
    text = TextBlock()
    reverse = blocks.BooleanBlock(required=False, help_text="Permet de d'intervertir le media et la zone de texte")
    section = blocks.BooleanBlock(required=False, help_text="Permet de sectionner la zone de texte")
    align = AlignTextChoiceBlock(required=False)
    media = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
            ('embed', EmbedWithSizeBlock()),
        ],
        max_num=1
    )
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=2
    )

    def mock(self, media='svg', align=None,
             section=False, reverse=False, size_media='m', button_1=constants.BUTTON_PRIMARY_FULL, button_2=None,
             *args, **kwargs):
        if media == 'svg':
            if 'theme' in kwargs:
                file = self.mocker.SVG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.SVG_SQUARE_SPACE
            else:
                file = self.mocker.SVG_SQUARE_SPACE
        else:
            if 'theme' in kwargs:
                file = self.mocker.IMG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.mocker.IMG_SQUARE_SPACE
            else:
                file = self.mocker.IMG_SQUARE_SPACE
        ret = {
            'type': 'media_text',
            'value': {
                'h2': self.mocker.h,
                'text': {
                    'value': self.mocker.normal
                },
                'media': [{
                    'type': media,
                    'value': {
                        'file': self.mocker.file(file).id,
                        'size': size_media
                    },
                }],
                'buttons': [],
                'reverse': reverse,
                'align': align,
                'section': section
            }
        }
        if media == 'embed':
            ret['value']['media'] = [{
                'type': 'embed',
                'value': {
                    'link': self.mocker.URL_EMBED,
                    'size': size_media
                }
            }]
        if button_1:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.mocker.button(button_1)
            })
        if button_2:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.mocker.button(m_type=button_2)
            })
        self.mock_data.update(ret)
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/media_text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Media Text"
