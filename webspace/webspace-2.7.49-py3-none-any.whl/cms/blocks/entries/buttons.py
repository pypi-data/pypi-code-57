from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms.blocks.common import ButtonBlock, EntryBlock


class ButtonsEntry(EntryBlock):
    align = AlignTextChoiceBlock(required=False)
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=3
    )

    def mock(self, btn_one=constants.BUTTON_SECONDARY_FULL, btn_two=constants.BUTTON_SECONDARY, align='left',
             *args, **kwargs):
        self.mock_data.update({
            'type': 'buttons',
            'value': {
                'buttons': [
                    {
                        'type': 'button',
                        'value': self.mocker.button(btn_one)
                    },
                    {
                        'type': 'button',
                        'value': self.mocker.button(btn_two)
                    },
                ],
                'align': align
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/buttons.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Buttons"
