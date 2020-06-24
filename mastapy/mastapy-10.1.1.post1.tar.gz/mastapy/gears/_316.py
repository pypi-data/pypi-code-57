'''_316.py

SpiralBevelRootLineTilt
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_ROOT_LINE_TILT = python_net_import('SMT.MastaAPI.Gears', 'SpiralBevelRootLineTilt')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelRootLineTilt',)


class SpiralBevelRootLineTilt(Enum):
    '''SpiralBevelRootLineTilt

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPIRAL_BEVEL_ROOT_LINE_TILT
    __hash__ = None

    ABOUT_MEAN_POINT = 0
    ABOUT_LARGE_END = 1
