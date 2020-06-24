'''_1446.py

NamedTuple
'''


from typing import Generic, TypeVar

from mastapy import _1
from mastapy._internal.python_net import python_net_import

_NAMED_TUPLE = python_net_import('SMT.MastaAPI.Utility.Generics', 'NamedTuple')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedTuple',)


T = TypeVar('T')


class NamedTuple(_1.APIBase, Generic[T]):
    '''NamedTuple

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _NAMED_TUPLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NamedTuple.TYPE'):
        super().__init__(instance_to_wrap)
