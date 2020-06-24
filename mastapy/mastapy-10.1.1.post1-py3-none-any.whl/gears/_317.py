'''_317.py

SpiralBevelToothTaper
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_TOOTH_TAPER = python_net_import('SMT.MastaAPI.Gears', 'SpiralBevelToothTaper')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelToothTaper',)


class SpiralBevelToothTaper(Enum):
    '''SpiralBevelToothTaper

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPIRAL_BEVEL_TOOTH_TAPER
    __hash__ = None

    DUPLEX_DPLX = 0
    STANDARD_STD = 1
    TILTED_ROOT_LINE_TRL = 2
    USERSPECIFIED = 3
