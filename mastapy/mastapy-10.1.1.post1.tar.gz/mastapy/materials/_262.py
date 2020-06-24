'''_262.py

MetalPlasticType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_METAL_PLASTIC_TYPE = python_net_import('SMT.MastaAPI.Materials', 'MetalPlasticType')


__docformat__ = 'restructuredtext en'
__all__ = ('MetalPlasticType',)


class MetalPlasticType(Enum):
    '''MetalPlasticType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _METAL_PLASTIC_TYPE
    __hash__ = None

    PLASTIC = 0
    METAL = 1
