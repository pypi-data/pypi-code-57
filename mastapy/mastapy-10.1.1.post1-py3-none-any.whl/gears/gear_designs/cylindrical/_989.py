'''_989.py

GearFitSystems
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GEAR_FIT_SYSTEMS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'GearFitSystems')


__docformat__ = 'restructuredtext en'
__all__ = ('GearFitSystems',)


class GearFitSystems(Enum):
    '''GearFitSystems

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _GEAR_FIT_SYSTEMS
    __hash__ = None

    NONE = 0
    DIN_39671978 = 1
