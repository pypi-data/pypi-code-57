'''_1071.py

DynamicsResponseType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_TYPE = python_net_import('SMT.MastaAPI.MathUtility', 'DynamicsResponseType')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicsResponseType',)


class DynamicsResponseType(Enum):
    '''DynamicsResponseType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _DYNAMICS_RESPONSE_TYPE

    __hash__ = None

    DISPLACEMENT = 0
    VELOCITY = 1
    ACCELERATION = 2
    FORCE = 3
    STRAIN_ENERGY = 4
    KINETIC_ENERGY = 5
    LINE_OF_ACTION_SEPARATION = 6
    DYNAMIC_MESH_FORCE = 7
    DYNAMIC_MESH_MOMENT = 8
    DYNAMIC_TE = 9
    ROOT_MEAN_SQUARED_NORMAL_DISPLACEMENT = 10
    ROOT_MEAN_SQUARED_NORMAL_VELOCITY = 11
    ROOT_MEAN_SQUARED_NORMAL_ACCELERATION = 12
    MAXIMUM_NORMAL_VELOCITY = 13
    AIRBORNE_SOUND_POWER = 14
    SOUND_INTENSITY = 15
    SOUND_PRESSURE = 16
