'''_1734.py

PowerLoadPIDControlSpeedInputType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_POWER_LOAD_PID_CONTROL_SPEED_INPUT_TYPE = python_net_import('SMT.MastaAPI.SystemModel', 'PowerLoadPIDControlSpeedInputType')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadPIDControlSpeedInputType',)


class PowerLoadPIDControlSpeedInputType(Enum):
    '''PowerLoadPIDControlSpeedInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _POWER_LOAD_PID_CONTROL_SPEED_INPUT_TYPE
    __hash__ = None

    CONSTANT_SPEED = 0
    SPEED_VS_TIME = 1
