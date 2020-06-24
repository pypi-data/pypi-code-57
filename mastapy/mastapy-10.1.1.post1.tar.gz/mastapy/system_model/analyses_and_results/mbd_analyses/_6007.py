'''_6007.py

ShapeOfInitialAccelerationPeriodForRunUp
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SHAPE_OF_INITIAL_ACCELERATION_PERIOD_FOR_RUN_UP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShapeOfInitialAccelerationPeriodForRunUp')


__docformat__ = 'restructuredtext en'
__all__ = ('ShapeOfInitialAccelerationPeriodForRunUp',)


class ShapeOfInitialAccelerationPeriodForRunUp(Enum):
    '''ShapeOfInitialAccelerationPeriodForRunUp

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SHAPE_OF_INITIAL_ACCELERATION_PERIOD_FOR_RUN_UP
    __hash__ = None

    QUADRATIC = 0
    CUBIC = 1
