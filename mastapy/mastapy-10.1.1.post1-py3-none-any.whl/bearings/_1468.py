'''_1468.py

BearingRadialInternalClearanceClass
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BEARING_RADIAL_INTERNAL_CLEARANCE_CLASS = python_net_import('SMT.MastaAPI.Bearings', 'BearingRadialInternalClearanceClass')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRadialInternalClearanceClass',)


class BearingRadialInternalClearanceClass(Enum):
    '''BearingRadialInternalClearanceClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BEARING_RADIAL_INTERNAL_CLEARANCE_CLASS
    __hash__ = None

    GROUP_2 = 0
    GROUP_N = 1
    GROUP_3 = 2
    GROUP_4 = 3
    GROUP_5 = 4
