'''_4894.py

ShaftComplexShape
'''


from typing import Generic, TypeVar

from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPLEX_SHAPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics', 'ShaftComplexShape')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftComplexShape',)


TLinearMeasurement = TypeVar('TLinearMeasurement', bound='_1035.MeasurementBase')
TAngularMeasurement = TypeVar('TAngularMeasurement', bound='_1035.MeasurementBase')


class ShaftComplexShape(_1.APIBase, Generic[TLinearMeasurement, TAngularMeasurement]):
    '''ShaftComplexShape

    This is a mastapy class.

    Generic Types:
        TLinearMeasurement
        TAngularMeasurement
    '''

    TYPE = _SHAFT_COMPLEX_SHAPE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftComplexShape.TYPE'):
        super().__init__(instance_to_wrap)
