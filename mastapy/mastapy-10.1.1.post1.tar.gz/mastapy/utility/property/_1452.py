'''_1452.py

EnumWithBool
'''


from enum import Enum
from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ENUM_WITH_BOOL = python_net_import('SMT.MastaAPI.Utility.Property', 'EnumWithBool')


__docformat__ = 'restructuredtext en'
__all__ = ('EnumWithBool',)


T = TypeVar('T', bound='Enum')


class EnumWithBool(_1.APIBase, Generic[T]):
    '''EnumWithBool

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _ENUM_WITH_BOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'EnumWithBool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
