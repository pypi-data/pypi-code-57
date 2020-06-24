'''_227.py

AGMALubricantType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_AGMA_LUBRICANT_TYPE = python_net_import('SMT.MastaAPI.Materials', 'AGMALubricantType')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMALubricantType',)


class AGMALubricantType(Enum):
    '''AGMALubricantType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _AGMA_LUBRICANT_TYPE
    __hash__ = None

    MINERAL_OIL = 0
    PAO_BASED_SYNTHETIC_NONVI_IMPROVED_OIL = 1
    PAG_BASED_SYNTHETIC = 2
    MILL7808K_GRADE_3 = 3
    MILL7808K_GRADE_4 = 4
    MILL23699E = 5
