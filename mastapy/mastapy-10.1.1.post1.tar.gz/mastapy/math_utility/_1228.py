'''_1228.py

PIDControlUpdateMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PID_CONTROL_UPDATE_METHOD = python_net_import('SMT.MastaAPI.MathUtility', 'PIDControlUpdateMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('PIDControlUpdateMethod',)


class PIDControlUpdateMethod(Enum):
    '''PIDControlUpdateMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _PID_CONTROL_UPDATE_METHOD
    __hash__ = None

    EACH_SOLVER_STEP = 0
    SAMPLE_TIME = 1
    CONTINUOUS = 2
