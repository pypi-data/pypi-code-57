'''_407.py

CylindricalMftFinishingMethods
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MFT_FINISHING_METHODS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalMftFinishingMethods')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMftFinishingMethods',)


class CylindricalMftFinishingMethods(Enum):
    '''CylindricalMftFinishingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CYLINDRICAL_MFT_FINISHING_METHODS

    __hash__ = None

    HOBBING = 0
    SHAPING = 1
    SHAVING = 2
    FORM_WHEEL_GRINDING = 3
    WORM_GRINDING = 4
    NONE = 5
    PLUNGE_SHAVING_WITH_MICROGEOMETRY = 6
