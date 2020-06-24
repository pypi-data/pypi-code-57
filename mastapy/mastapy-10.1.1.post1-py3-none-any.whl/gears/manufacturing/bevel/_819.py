'''_819.py

MachineTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MACHINE_TYPES = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'MachineTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('MachineTypes',)


class MachineTypes(Enum):
    '''MachineTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MACHINE_TYPES
    __hash__ = None

    CRADLE_STYLE = 0
    PHOENIX_STYLE = 1
