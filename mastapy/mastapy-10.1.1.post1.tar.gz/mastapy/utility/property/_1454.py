'''_1454.py

TypedObjectsWithOption
'''


from typing import Generic, TypeVar

from mastapy import _1
from mastapy._internal.python_net import python_net_import

_TYPED_OBJECTS_WITH_OPTION = python_net_import('SMT.MastaAPI.Utility.Property', 'TypedObjectsWithOption')


__docformat__ = 'restructuredtext en'
__all__ = ('TypedObjectsWithOption',)


T = TypeVar('T')


class TypedObjectsWithOption(_1.APIBase, Generic[T]):
    '''TypedObjectsWithOption

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _TYPED_OBJECTS_WITH_OPTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TypedObjectsWithOption.TYPE'):
        super().__init__(instance_to_wrap)
