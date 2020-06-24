'''_65.py

SurfaceFinishes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SURFACE_FINISHES = python_net_import('SMT.MastaAPI.Shafts', 'SurfaceFinishes')


__docformat__ = 'restructuredtext en'
__all__ = ('SurfaceFinishes',)


class SurfaceFinishes(Enum):
    '''SurfaceFinishes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SURFACE_FINISHES
    __hash__ = None

    HIGHLY_POLISHED_NOMINAL = 0
    POLISHED = 1
    GROUND = 2
    COLD_DRAWN_OR_MACHINED_63UIN_16UM = 3
    COLD_DRAWN_OR_MACHINED_125UIN_32UM = 4
    COLD_DRAWN_OR_MACHINED_250UIN_63UM = 5
    COLD_DRAWN_OR_MACHINED_500UIN_125UM = 6
    HOT_ROLLED = 7
    FORGED = 8
    USER_SPECIFIED = 9
