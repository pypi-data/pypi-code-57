'''_2264.py

AbstractShaftOrHousingLoadCase
'''


from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _6003
from mastapy.system_model.part_model import _1906, _1924
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.analyses_and_results.static_loads import _2268
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AbstractShaftOrHousingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingLoadCase',)


class AbstractShaftOrHousingLoadCase(_2268.ComponentLoadCase):
    '''AbstractShaftOrHousingLoadCase

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rayleigh_damping_alpha(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RayleighDampingAlpha' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RayleighDampingAlpha) if self.wrapped.RayleighDampingAlpha else None

    @rayleigh_damping_alpha.setter
    def rayleigh_damping_alpha(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RayleighDampingAlpha = value

    @property
    def include_flexibilities_setting(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption: 'IncludeFlexibilitiesSetting' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption)(self.wrapped.IncludeFlexibilitiesSetting) if self.wrapped.IncludeFlexibilitiesSetting else None

    @include_flexibilities_setting.setter
    def include_flexibilities_setting(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.IncludeFlexibilitiesSetting = value

    @property
    def component_design(self) -> '_1906.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1906.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ImportedFEComponent':
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Shaft':
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
