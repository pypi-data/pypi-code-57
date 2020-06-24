'''_1450.py

DutyCyclePropertySummarySmallAngle
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.utility.property import _1447
from mastapy.utility.units_and_measurements.measurements import _1283
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_PROPERTY_SUMMARY_SMALL_ANGLE = python_net_import('SMT.MastaAPI.Utility.Property', 'DutyCyclePropertySummarySmallAngle')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCyclePropertySummarySmallAngle',)


T = TypeVar('T')


class DutyCyclePropertySummarySmallAngle(_1447.DutyCyclePropertySummary['_1283.AngleSmall', 'T'], Generic[T]):
    '''DutyCyclePropertySummarySmallAngle

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _DUTY_CYCLE_PROPERTY_SUMMARY_SMALL_ANGLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCyclePropertySummarySmallAngle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def maximum_value(self) -> 'float':
        '''float: 'MaximumValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumValue

    @property
    def minimum_value(self) -> 'float':
        '''float: 'MinimumValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumValue

    @property
    def average_value(self) -> 'float':
        '''float: 'AverageValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageValue
