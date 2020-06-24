'''_1035.py

MeasurementBase
'''


from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.utility.units_and_measurements import _1385
from mastapy.utility import _1272
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_BASE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'MeasurementBase')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementBase',)


class MeasurementBase(_1.APIBase):
    '''MeasurementBase

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def default_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        '''list_with_selected_item.ListWithSelectedItem_Unit: 'DefaultUnit' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Unit)(self.wrapped.DefaultUnit) if self.wrapped.DefaultUnit else None

    @default_unit.setter
    def default_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.DefaultUnit = value

    @property
    def rounding_digits(self) -> 'int':
        '''int: 'RoundingDigits' is the original name of this property.'''

        return self.wrapped.RoundingDigits

    @rounding_digits.setter
    def rounding_digits(self, value: 'int'):
        self.wrapped.RoundingDigits = int(value) if value else 0

    @property
    def rounding_method(self) -> '_1272.RoundingMethods':
        '''RoundingMethods: 'RoundingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RoundingMethod)
        return constructor.new(_1272.RoundingMethods)(value) if value else None

    @rounding_method.setter
    def rounding_method(self, value: '_1272.RoundingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RoundingMethod = value

    @property
    def absolute_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AbsoluteTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AbsoluteTolerance) if self.wrapped.AbsoluteTolerance else None

    @absolute_tolerance.setter
    def absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AbsoluteTolerance = value

    @property
    def percentage_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PercentageTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PercentageTolerance) if self.wrapped.PercentageTolerance else None

    @percentage_tolerance.setter
    def percentage_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PercentageTolerance = value

    @property
    def current_unit(self) -> '_1385.Unit':
        '''Unit: 'CurrentUnit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1385.Unit)(self.wrapped.CurrentUnit) if self.wrapped.CurrentUnit else None
