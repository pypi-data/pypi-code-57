'''_1453.py

NamedRangeWithOverridableMinAndMax
'''


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_NAMED_RANGE_WITH_OVERRIDABLE_MIN_AND_MAX = python_net_import('SMT.MastaAPI.Utility.Property', 'NamedRangeWithOverridableMinAndMax')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedRangeWithOverridableMinAndMax',)


T = TypeVar('T', bound='')
TMeasurement = TypeVar('TMeasurement', bound='_1035.MeasurementBase')


class NamedRangeWithOverridableMinAndMax(_1.APIBase, Generic[T, TMeasurement]):
    '''NamedRangeWithOverridableMinAndMax

    This is a mastapy class.

    Generic Types:
        T
        TMeasurement
    '''

    TYPE = _NAMED_RANGE_WITH_OVERRIDABLE_MIN_AND_MAX
    __hash__ = None

    def __init__(self, instance_to_wrap: 'NamedRangeWithOverridableMinAndMax.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def min(self) -> 'overridable.Overridable_T':
        '''overridable.Overridable_T: 'Min' is the original name of this property.'''

        return constructor.new(overridable.Overridable_T)(self.wrapped.Min) if self.wrapped.Min else None

    @min.setter
    def min(self, value: 'overridable.Overridable_T.implicit_type()'):
        wrapper_type = overridable.Overridable_T.TYPE
        enclosed_type = overridable.Overridable_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Min = value

    @property
    def max(self) -> 'overridable.Overridable_T':
        '''overridable.Overridable_T: 'Max' is the original name of this property.'''

        return constructor.new(overridable.Overridable_T)(self.wrapped.Max) if self.wrapped.Max else None

    @max.setter
    def max(self, value: 'overridable.Overridable_T.implicit_type()'):
        wrapper_type = overridable.Overridable_T.TYPE
        enclosed_type = overridable.Overridable_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Max = value
