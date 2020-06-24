'''_113.py

AbstractVaryingInputComponent
'''


from mastapy._internal.implicit import enum_with_selected_value
from mastapy.nodal_analysis import _111
from mastapy._internal import constructor
from mastapy.nodal_analysis.varying_input_components import _118
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ABSTRACT_VARYING_INPUT_COMPONENT = python_net_import('SMT.MastaAPI.NodalAnalysis.VaryingInputComponents', 'AbstractVaryingInputComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractVaryingInputComponent',)


class AbstractVaryingInputComponent(_1.APIBase):
    '''AbstractVaryingInputComponent

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_VARYING_INPUT_COMPONENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractVaryingInputComponent.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def input_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ValueInputOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ValueInputOption: 'InputType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ValueInputOption)(self.wrapped.InputType) if self.wrapped.InputType else None

    @input_type.setter
    def input_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ValueInputOption.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ValueInputOption.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ValueInputOption.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.InputType = value

    @property
    def time_profile_repeats(self) -> 'bool':
        '''bool: 'TimeProfileRepeats' is the original name of this property.'''

        return self.wrapped.TimeProfileRepeats

    @time_profile_repeats.setter
    def time_profile_repeats(self, value: 'bool'):
        self.wrapped.TimeProfileRepeats = bool(value) if value else False

    @property
    def single_point_selection_method_for_value_vs_time(self) -> 'enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod: 'SinglePointSelectionMethodForValueVsTime' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod)(self.wrapped.SinglePointSelectionMethodForValueVsTime) if self.wrapped.SinglePointSelectionMethodForValueVsTime else None

    @single_point_selection_method_for_value_vs_time.setter
    def single_point_selection_method_for_value_vs_time(self, value: 'enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SinglePointSelectionMethod.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.SinglePointSelectionMethodForValueVsTime = value

    @property
    def include_values_before_zero_time(self) -> 'bool':
        '''bool: 'IncludeValuesBeforeZeroTime' is the original name of this property.'''

        return self.wrapped.IncludeValuesBeforeZeroTime

    @include_values_before_zero_time.setter
    def include_values_before_zero_time(self, value: 'bool'):
        self.wrapped.IncludeValuesBeforeZeroTime = bool(value) if value else False
