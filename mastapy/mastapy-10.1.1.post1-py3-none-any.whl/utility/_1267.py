'''_1267.py

InputNamePrompter
'''


from mastapy._internal import constructor
from mastapy.utility.model_validation import _1380
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_INPUT_NAME_PROMPTER = python_net_import('SMT.MastaAPI.Utility', 'InputNamePrompter')


__docformat__ = 'restructuredtext en'
__all__ = ('InputNamePrompter',)


class InputNamePrompter(_1.APIBase):
    '''InputNamePrompter

    This is a mastapy class.
    '''

    TYPE = _INPUT_NAME_PROMPTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'InputNamePrompter.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def title(self) -> 'str':
        '''str: 'Title' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Title

    @property
    def input_name(self) -> 'str':
        '''str: 'InputName' is the original name of this property.'''

        return self.wrapped.InputName

    @input_name.setter
    def input_name(self, value: 'str'):
        self.wrapped.InputName = str(value) if value else None

    @property
    def status(self) -> '_1380.Status':
        '''Status: 'Status' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1380.Status)(self.wrapped.Status) if self.wrapped.Status else None
