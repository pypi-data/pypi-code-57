from wagtail.core import blocks

from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    ButtonBlock, EntryBlock


class FirstContentEntry(EntryBlock):
    h1 = blocks.CharBlock()
    text = TextBlock()
    align = AlignTextChoiceBlock(required=False)
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=2,
        required=False
    )

    def mock(self, align='left', button_1=constants.BUTTON_PRIMARY,
             button_2=constants.BUTTON_PRIMARY_FULL, *args, **kwargs):
        self.mock_data.update({
            'type': 'first_content',
            'value': {
                'h1': self.mocker.h,
                'text': {
                    'value': self.mocker.text_first_content,
                },
                'buttons': [{
                    'type': 'button',
                    'value': self.mocker.button(button_1)
                }, {
                    'type': 'button',
                    'value': self.mocker.button(button_2)
                }],
                'align': align
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/first_content.html' % constants.BLOCK_TEMPLATES_PATH
        label = "First Content"
