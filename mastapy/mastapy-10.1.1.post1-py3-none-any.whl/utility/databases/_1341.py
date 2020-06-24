'''_1341.py

NamedDatabase
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.utility.databases import _1342, _1344, _1343
from mastapy._internal.python_net import python_net_import

_NAMED_DATABASE = python_net_import('SMT.MastaAPI.Utility.Databases', 'NamedDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedDatabase',)


TValue = TypeVar('TValue', bound='_1342.NamedDatabaseItem')


class NamedDatabase(_1344.SQLDatabase['_1343.NamedKey', 'TValue'], Generic[TValue]):
    '''NamedDatabase

    This is a mastapy class.

    Generic Types:
        TValue
    '''

    TYPE = _NAMED_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'NamedDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    def create(self, name: 'str') -> 'TValue':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            TValue
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(TValue)(method_result) if method_result else None

    def get_value(self, name: 'str') -> 'TValue':
        ''' 'GetValue' is the original name of this method.

        Args:
            name (str)

        Returns:
            TValue
        '''

        name = str(name)
        method_result = self.wrapped.GetValue(name if name else None)
        return constructor.new(TValue)(method_result) if method_result else None

    def rename(self, item: '_1342.NamedDatabaseItem', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            item (mastapy.utility.databases.NamedDatabaseItem)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(item.wrapped if item else None, new_name if new_name else None)
        return method_result
