'''_285.py

InternalExternalType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_INTERNAL_EXTERNAL_TYPE = python_net_import('SMT.MastaAPI.Geometry.TwoD', 'InternalExternalType')


__docformat__ = 'restructuredtext en'
__all__ = ('InternalExternalType',)


class InternalExternalType(Enum):
    '''InternalExternalType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _INTERNAL_EXTERNAL_TYPE
    __hash__ = None

    INTERNAL = 0
    EXTERNAL = 1
