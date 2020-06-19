from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    EntryBlock


class TextEntry(EntryBlock):
    text = TextBlock()
    align = AlignTextChoiceBlock(required=False)

    def mock(self, txt=None, size='big', align=None, *args, **kwargs):
        self.mock_data.update({
            'type': 'text',
            'value': {
                'text': {
                    'value': txt if txt else eval('self.mocker.' + size),
                },
                'align': align
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Text"
        icon = 'edit'
