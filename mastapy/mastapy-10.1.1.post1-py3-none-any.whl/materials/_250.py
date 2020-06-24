'''_250.py

HardnessType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_HARDNESS_TYPE = python_net_import('SMT.MastaAPI.Materials', 'HardnessType')


__docformat__ = 'restructuredtext en'
__all__ = ('HardnessType',)


class HardnessType(Enum):
    '''HardnessType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _HARDNESS_TYPE
    __hash__ = None

    BRINELL_3000KG_HB = 0
    VICKERS_HV = 1
    ROCKWELL_C_HRC = 2
