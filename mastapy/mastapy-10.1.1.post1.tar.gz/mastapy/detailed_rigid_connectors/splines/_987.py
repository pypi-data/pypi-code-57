'''_987.py

PressureAngleTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PRESSURE_ANGLE_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'PressureAngleTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('PressureAngleTypes',)


class PressureAngleTypes(Enum):
    '''PressureAngleTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _PRESSURE_ANGLE_TYPES

    __hash__ = None

    _30 = 0
    _375 = 1
    _45 = 2
