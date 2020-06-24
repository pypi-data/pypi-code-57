'''_1011.py

ConicalMachineSettingCalculationMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONICAL_MACHINE_SETTING_CALCULATION_METHODS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalMachineSettingCalculationMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMachineSettingCalculationMethods',)


class ConicalMachineSettingCalculationMethods(Enum):
    '''ConicalMachineSettingCalculationMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CONICAL_MACHINE_SETTING_CALCULATION_METHODS
    __hash__ = None

    GLEASON = 0
    SMT = 1
    SPECIFIED = 2
