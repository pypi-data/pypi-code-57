'''_1428.py

StatusItem
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_STATUS_ITEM = python_net_import('SMT.MastaAPI.Utility.ModelValidation', 'StatusItem')


__docformat__ = 'restructuredtext en'
__all__ = ('StatusItem',)


class StatusItem(_1.APIBase):
    '''StatusItem

    This is a mastapy class.
    '''

    TYPE = _STATUS_ITEM
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StatusItem.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def description(self) -> 'str':
        '''str: 'Description' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Description
