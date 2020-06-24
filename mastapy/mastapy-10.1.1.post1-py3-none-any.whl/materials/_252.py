'''_252.py

ISOLubricantType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ISO_LUBRICANT_TYPE = python_net_import('SMT.MastaAPI.Materials', 'ISOLubricantType')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOLubricantType',)


class ISOLubricantType(Enum):
    '''ISOLubricantType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ISO_LUBRICANT_TYPE
    __hash__ = None

    MINERAL_OIL = 0
    WATER_SOLUBLE_POLYGLYCOL = 1
    NON_WATER_SOLUBLE_POLYGLYCOL = 2
    POLYALFAOLEFIN = 3
    PHOSPHATE_ESTER = 4
    TRACTION_FLUID = 5
