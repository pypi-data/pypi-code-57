'''_1732.py

PowerLoadDragTorqueSpecificationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_POWER_LOAD_DRAG_TORQUE_SPECIFICATION_METHOD = python_net_import('SMT.MastaAPI.SystemModel', 'PowerLoadDragTorqueSpecificationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadDragTorqueSpecificationMethod',)


class PowerLoadDragTorqueSpecificationMethod(Enum):
    '''PowerLoadDragTorqueSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _POWER_LOAD_DRAG_TORQUE_SPECIFICATION_METHOD
    __hash__ = None

    DRAG_TORQUE_FOR_TIME_AND_SPEED = 0
    SPEED_POLYNOMIAL_COEFFICIENTS = 1
    CALCULATED_LINEAR_RESISTANCE_FOR_STEADY_SPEED = 2
    CALCULATED_QUADRATIC_RESISTANCE_FOR_STEADY_SPEED = 3
