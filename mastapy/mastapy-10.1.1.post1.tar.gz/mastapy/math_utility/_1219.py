'''_1219.py

DynamicsResponse3DChartType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_3D_CHART_TYPE = python_net_import('SMT.MastaAPI.MathUtility', 'DynamicsResponse3DChartType')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicsResponse3DChartType',)


class DynamicsResponse3DChartType(Enum):
    '''DynamicsResponse3DChartType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _DYNAMICS_RESPONSE_3D_CHART_TYPE
    __hash__ = None

    WATERFALL_FREQUENCY_AND_SPEED = 0
    ORDER_MAP_ORDER_AND_SPEED = 1
