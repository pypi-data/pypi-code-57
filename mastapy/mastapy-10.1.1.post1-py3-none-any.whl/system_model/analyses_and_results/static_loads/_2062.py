'''_2062.py

TorqueRippleInputType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TORQUE_RIPPLE_INPUT_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'TorqueRippleInputType')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueRippleInputType',)


class TorqueRippleInputType(Enum):
    '''TorqueRippleInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TORQUE_RIPPLE_INPUT_TYPE
    __hash__ = None

    ROTOR_TORQUE_RIPPLE_TIME_SERIES = 0
    STATOR_TEETH_TANGENTIAL_LOADS = 1
    CONSTANT_TORQUE_NO_TORQUE_RIPPLE = 2
