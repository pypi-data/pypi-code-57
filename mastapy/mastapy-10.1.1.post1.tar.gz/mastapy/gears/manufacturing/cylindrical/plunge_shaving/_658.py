'''_658.py

PlungeShaverOutputs
'''


from mastapy.scripting import _732
from mastapy._internal import constructor
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _650, _656
from mastapy.gears.manufacturing.cylindrical import _631
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_OUTPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverOutputs')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverOutputs',)


class PlungeShaverOutputs(_1.APIBase):
    '''PlungeShaverOutputs

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_OUTPUTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverOutputs.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def profile_modification_on_conjugate_shaver_chart_left_flank(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ProfileModificationOnConjugateShaverChartLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ProfileModificationOnConjugateShaverChartLeftFlank) if self.wrapped.ProfileModificationOnConjugateShaverChartLeftFlank else None

    @property
    def profile_modification_on_conjugate_shaver_chart_right_flank(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ProfileModificationOnConjugateShaverChartRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ProfileModificationOnConjugateShaverChartRightFlank) if self.wrapped.ProfileModificationOnConjugateShaverChartRightFlank else None

    @property
    def shaver_profile_modification_z_plane(self) -> 'float':
        '''float: 'ShaverProfileModificationZPlane' is the original name of this property.'''

        return self.wrapped.ShaverProfileModificationZPlane

    @shaver_profile_modification_z_plane.setter
    def shaver_profile_modification_z_plane(self, value: 'float'):
        self.wrapped.ShaverProfileModificationZPlane = float(value) if value else 0.0

    @property
    def shaved_gear_profile_modification_z_plane(self) -> 'float':
        '''float: 'ShavedGearProfileModificationZPlane' is the original name of this property.'''

        return self.wrapped.ShavedGearProfileModificationZPlane

    @shaved_gear_profile_modification_z_plane.setter
    def shaved_gear_profile_modification_z_plane(self, value: 'float'):
        self.wrapped.ShavedGearProfileModificationZPlane = float(value) if value else 0.0

    @property
    def difference_between_chart_z_plane(self) -> 'float':
        '''float: 'DifferenceBetweenChartZPlane' is the original name of this property.'''

        return self.wrapped.DifferenceBetweenChartZPlane

    @difference_between_chart_z_plane.setter
    def difference_between_chart_z_plane(self, value: 'float'):
        self.wrapped.DifferenceBetweenChartZPlane = float(value) if value else 0.0

    @property
    def chart(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ChartType':
        '''enum_with_selected_value.EnumWithSelectedValue_ChartType: 'Chart' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ChartType)(self.wrapped.Chart) if self.wrapped.Chart else None

    @chart.setter
    def chart(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ChartType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ChartType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ChartType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.Chart = value

    @property
    def selected_flank(self) -> 'enum_with_selected_value.EnumWithSelectedValue_Flank':
        '''enum_with_selected_value.EnumWithSelectedValue_Flank: 'SelectedFlank' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_Flank)(self.wrapped.SelectedFlank) if self.wrapped.SelectedFlank else None

    @selected_flank.setter
    def selected_flank(self, value: 'enum_with_selected_value.EnumWithSelectedValue_Flank.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_Flank.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_Flank.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.SelectedFlank = value

    @property
    def calculation_details(self) -> '_656.PlungeShaverGeneration':
        '''PlungeShaverGeneration: 'CalculationDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_656.PlungeShaverGeneration)(self.wrapped.CalculationDetails) if self.wrapped.CalculationDetails else None
