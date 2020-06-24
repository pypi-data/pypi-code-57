'''_1696.py

RollerBearing
'''


from typing import List

from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal import constructor, conversion
from mastapy.bearings import _1480
from mastapy.bearings.roller_bearing_profiles import _1504, _1514
from mastapy.bearings.bearing_designs.rolling import _1699
from mastapy._internal.python_net import python_net_import

_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'RollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerBearing',)


class RollerBearing(_1699.RollingBearing):
    '''RollerBearing

    This is a mastapy class.
    '''

    TYPE = _ROLLER_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollerBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def element_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementDiameter) if self.wrapped.ElementDiameter else None

    @element_diameter.setter
    def element_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementDiameter = value

    @property
    def roller_length(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RollerLength' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RollerLength) if self.wrapped.RollerLength else None

    @roller_length.setter
    def roller_length(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RollerLength = value

    @property
    def element_effective_length(self) -> 'float':
        '''float: 'ElementEffectiveLength' is the original name of this property.'''

        return self.wrapped.ElementEffectiveLength

    @element_effective_length.setter
    def element_effective_length(self, value: 'float'):
        self.wrapped.ElementEffectiveLength = float(value) if value else 0.0

    @property
    def corner_radii(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CornerRadii' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CornerRadii) if self.wrapped.CornerRadii else None

    @corner_radii.setter
    def corner_radii(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.CornerRadii = value

    @property
    def roller_profile(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes':
        '''enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes: 'RollerProfile' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes)(self.wrapped.RollerProfile) if self.wrapped.RollerProfile else None

    @roller_profile.setter
    def roller_profile(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.RollerProfile = value

    @property
    def iso2812007_dynamic_equivalent_load_factors_can_be_specified(self) -> 'bool':
        '''bool: 'ISO2812007DynamicEquivalentLoadFactorsCanBeSpecified' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO2812007DynamicEquivalentLoadFactorsCanBeSpecified

    @property
    def iso2812007_dynamic_radial_load_factor_for_low_axial_radial_load_ratios(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ISO2812007DynamicRadialLoadFactorForLowAxialRadialLoadRatios' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ISO2812007DynamicRadialLoadFactorForLowAxialRadialLoadRatios) if self.wrapped.ISO2812007DynamicRadialLoadFactorForLowAxialRadialLoadRatios else None

    @iso2812007_dynamic_radial_load_factor_for_low_axial_radial_load_ratios.setter
    def iso2812007_dynamic_radial_load_factor_for_low_axial_radial_load_ratios(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ISO2812007DynamicRadialLoadFactorForLowAxialRadialLoadRatios = value

    @property
    def iso2812007_dynamic_axial_load_factor_for_low_axial_radial_load_ratios(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ISO2812007DynamicAxialLoadFactorForLowAxialRadialLoadRatios' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ISO2812007DynamicAxialLoadFactorForLowAxialRadialLoadRatios) if self.wrapped.ISO2812007DynamicAxialLoadFactorForLowAxialRadialLoadRatios else None

    @iso2812007_dynamic_axial_load_factor_for_low_axial_radial_load_ratios.setter
    def iso2812007_dynamic_axial_load_factor_for_low_axial_radial_load_ratios(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ISO2812007DynamicAxialLoadFactorForLowAxialRadialLoadRatios = value

    @property
    def iso2812007_dynamic_radial_load_factor_for_high_axial_radial_load_ratios(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ISO2812007DynamicRadialLoadFactorForHighAxialRadialLoadRatios' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ISO2812007DynamicRadialLoadFactorForHighAxialRadialLoadRatios) if self.wrapped.ISO2812007DynamicRadialLoadFactorForHighAxialRadialLoadRatios else None

    @iso2812007_dynamic_radial_load_factor_for_high_axial_radial_load_ratios.setter
    def iso2812007_dynamic_radial_load_factor_for_high_axial_radial_load_ratios(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ISO2812007DynamicRadialLoadFactorForHighAxialRadialLoadRatios = value

    @property
    def iso2812007_dynamic_axial_load_factor_for_high_axial_radial_load_ratios(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ISO2812007DynamicAxialLoadFactorForHighAxialRadialLoadRatios' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ISO2812007DynamicAxialLoadFactorForHighAxialRadialLoadRatios) if self.wrapped.ISO2812007DynamicAxialLoadFactorForHighAxialRadialLoadRatios else None

    @iso2812007_dynamic_axial_load_factor_for_high_axial_radial_load_ratios.setter
    def iso2812007_dynamic_axial_load_factor_for_high_axial_radial_load_ratios(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ISO2812007DynamicAxialLoadFactorForHighAxialRadialLoadRatios = value

    @property
    def roller_profile_set(self) -> '_1504.ProfileSet':
        '''ProfileSet: 'RollerProfileSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1504.ProfileSet)(self.wrapped.RollerProfileSet) if self.wrapped.RollerProfileSet else None

    @property
    def outer_race_profile_set(self) -> '_1504.ProfileSet':
        '''ProfileSet: 'OuterRaceProfileSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1504.ProfileSet)(self.wrapped.OuterRaceProfileSet) if self.wrapped.OuterRaceProfileSet else None

    @property
    def inner_race_profile_set(self) -> '_1504.ProfileSet':
        '''ProfileSet: 'InnerRaceProfileSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1504.ProfileSet)(self.wrapped.InnerRaceProfileSet) if self.wrapped.InnerRaceProfileSet else None

    @property
    def inner_race_and_roller_profiles(self) -> 'List[_1514.RollerRaceProfilePoint]':
        '''List[RollerRaceProfilePoint]: 'InnerRaceAndRollerProfiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InnerRaceAndRollerProfiles, constructor.new(_1514.RollerRaceProfilePoint))
        return value

    @property
    def outer_race_and_roller_profiles(self) -> 'List[_1514.RollerRaceProfilePoint]':
        '''List[RollerRaceProfilePoint]: 'OuterRaceAndRollerProfiles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OuterRaceAndRollerProfiles, constructor.new(_1514.RollerRaceProfilePoint))
        return value

    @property
    def inner_race_and_roller_profiles_for_first_row(self) -> 'List[_1514.RollerRaceProfilePoint]':
        '''List[RollerRaceProfilePoint]: 'InnerRaceAndRollerProfilesForFirstRow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InnerRaceAndRollerProfilesForFirstRow, constructor.new(_1514.RollerRaceProfilePoint))
        return value

    @property
    def outer_race_and_roller_profiles_for_first_row(self) -> 'List[_1514.RollerRaceProfilePoint]':
        '''List[RollerRaceProfilePoint]: 'OuterRaceAndRollerProfilesForFirstRow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OuterRaceAndRollerProfilesForFirstRow, constructor.new(_1514.RollerRaceProfilePoint))
        return value

    @property
    def inner_race_and_roller_profiles_for_second_row(self) -> 'List[_1514.RollerRaceProfilePoint]':
        '''List[RollerRaceProfilePoint]: 'InnerRaceAndRollerProfilesForSecondRow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InnerRaceAndRollerProfilesForSecondRow, constructor.new(_1514.RollerRaceProfilePoint))
        return value

    @property
    def outer_race_and_roller_profiles_for_second_row(self) -> 'List[_1514.RollerRaceProfilePoint]':
        '''List[RollerRaceProfilePoint]: 'OuterRaceAndRollerProfilesForSecondRow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OuterRaceAndRollerProfilesForSecondRow, constructor.new(_1514.RollerRaceProfilePoint))
        return value
