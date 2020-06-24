'''_1264.py

FileHistory
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.utility import _1265
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FILE_HISTORY = python_net_import('SMT.MastaAPI.Utility', 'FileHistory')


__docformat__ = 'restructuredtext en'
__all__ = ('FileHistory',)


class FileHistory(_1.APIBase):
    '''FileHistory

    This is a mastapy class.
    '''

    TYPE = _FILE_HISTORY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FileHistory.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clear_history(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearHistory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearHistory

    @property
    def number_of_history_items(self) -> 'int':
        '''int: 'NumberOfHistoryItems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfHistoryItems

    @property
    def items(self) -> 'List[_1265.FileHistoryItem]':
        '''List[FileHistoryItem]: 'Items' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Items, constructor.new(_1265.FileHistoryItem))
        return value
