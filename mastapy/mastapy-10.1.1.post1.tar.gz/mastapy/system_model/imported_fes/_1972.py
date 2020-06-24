'''_1972.py

ThermalExpansionOption
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_THERMAL_EXPANSION_OPTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ThermalExpansionOption')


__docformat__ = 'restructuredtext en'
__all__ = ('ThermalExpansionOption',)


class ThermalExpansionOption(Enum):
    '''ThermalExpansionOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _THERMAL_EXPANSION_OPTION

    __hash__ = None

    UNIFORM = 0
    SPECIFIED_FORCE = 1
    SPECIFIED_DISPLACEMENT = 2
    CALCULATED_USING_MATERIAL_PROPERTIES = 3
