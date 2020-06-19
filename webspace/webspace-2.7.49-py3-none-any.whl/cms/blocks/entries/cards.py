from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import \
    SvgWithSizeBlock, \
    TextBlock, \
    ButtonBlock, \
    EntryBlock, \
    ImageWithSizeBlock


class CustomCard(blocks.StructBlock):
    text = TextBlock()
    button = ButtonBlock()
    icon = SvgWithSizeBlock()
    media = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
        ],
        max_num=1,
        required=False
    )

    class Meta:
        template = '%s/common/custom_card.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Custom Card"


class CardsEntry(EntryBlock):
    amp_scripts = ['carousel']
    carousel = blocks.BooleanBlock(required=False)
    carousel_cta = blocks.BooleanBlock(required=False, default=True)
    cards = blocks.StreamBlock(
        [
            ('custom', CustomCard()),
        ],
        min_num=1
    )

    def mock(self, stop=None, carousel=True, *args, **kwargs):
        if 'theme' in kwargs:
            icon = self.mocker.SVG_ICON_LIGHT if kwargs['theme'] == constants.THEME_LIGHT \
                else self.mocker.SVG_ICON_SPACE
            file = self.mocker.SVG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT \
                else self.mocker.SVG_SQUARE_SPACE

        else:
            icon = self.mocker.SVG_ICON_SPACE
            file = self.mocker.SVG_SQUARE_SPACE
        ret = {
            'type': 'cards',
            'value': {
                'cards': [],
                'carousel': carousel
            }
        }
        cci = {
            'text': {
                'value': self.mocker.xs,
                'align': 'center'
            },
            'button': self.mocker.button(constants.BUTTON_SECONDARY)
        }
        if self.random_counter % 2:
            cci['media'] = [{
                'type': 'svg',
                'value': {
                    'file': self.mocker.file(file).id,
                    'size': 'full'
                },
            }]
        else:
            cci['icon'] = {
                'file': self.mocker.file(icon).id,
                'size': 'l'
            }
        card_custom = [cci, cci, cci, cci, cci, cci, cci]
        i = 0
        for card_item in card_custom:
            if not carousel and stop and i == stop:
                break
            ret['value']['cards'].append({
                'type': 'custom',
                'value': {
                    'custom': card_item
                }
            })
            ret['value']['cards'][i]['value'] = card_item
            i += 1
        self.mock_data.update(ret)
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/cards.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Cards"
        #  icon = 'image'
