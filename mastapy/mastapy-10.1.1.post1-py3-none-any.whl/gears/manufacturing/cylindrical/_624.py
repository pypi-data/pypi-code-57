'''_624.py

CylindricalMftRoughingMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MFT_ROUGHING_METHODS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalMftRoughingMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMftRoughingMethods',)


class CylindricalMftRoughingMethods(Enum):
    '''CylindricalMftRoughingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CYLINDRICAL_MFT_ROUGHING_METHODS
    __hash__ = None

    HOBBING = 0
    SHAPING = 1
