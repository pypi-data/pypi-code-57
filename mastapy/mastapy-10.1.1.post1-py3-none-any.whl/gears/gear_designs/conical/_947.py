'''_947.py

ConicalManufactureMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONICAL_MANUFACTURE_METHODS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalManufactureMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalManufactureMethods',)


class ConicalManufactureMethods(Enum):
    '''ConicalManufactureMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CONICAL_MANUFACTURE_METHODS
    __hash__ = None

    FORMATE_TILT = 0
    FORMATE_MODIFIED_ROLL = 1
    GENERATING_TILT = 2
    GENERATING_TILT_WITH_OFFSET = 3
    GENERATING_MODIFIED_ROLL = 4
    HELIXFORM = 5
