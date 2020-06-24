'''_833.py

WheelFormatMachineTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WHEEL_FORMAT_MACHINE_TYPES = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'WheelFormatMachineTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('WheelFormatMachineTypes',)


class WheelFormatMachineTypes(Enum):
    '''WheelFormatMachineTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WHEEL_FORMAT_MACHINE_TYPES
    __hash__ = None

    COMPATIBLE_WITH_NO608_609_610 = 0
    COMPATIBLE_WITH_NO606_607 = 1
    UNKNOWN = 2
