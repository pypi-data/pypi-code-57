'''_1048.py

MicroGeometryViewingOptions
'''


from typing import Callable

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1031
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.ltca import _852
from mastapy.nodal_analysis import _114
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_VIEWING_OPTIONS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'MicroGeometryViewingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryViewingOptions',)


class MicroGeometryViewingOptions(_1.APIBase):
    '''MicroGeometryViewingOptions

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_VIEWING_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryViewingOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def show_force_arrows(self) -> 'bool':
        '''bool: 'ShowForceArrows' is the original name of this property.'''

        return self.wrapped.ShowForceArrows

    @show_force_arrows.setter
    def show_force_arrows(self, value: 'bool'):
        self.wrapped.ShowForceArrows = bool(value) if value else False

    @property
    def show_contact_chart(self) -> 'bool':
        '''bool: 'ShowContactChart' is the original name of this property.'''

        return self.wrapped.ShowContactChart

    @show_contact_chart.setter
    def show_contact_chart(self, value: 'bool'):
        self.wrapped.ShowContactChart = bool(value) if value else False

    @property
    def edit_contact_patch_legend(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'EditContactPatchLegend' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EditContactPatchLegend

    @property
    def show_root_stress_chart(self) -> 'bool':
        '''bool: 'ShowRootStressChart' is the original name of this property.'''

        return self.wrapped.ShowRootStressChart

    @show_root_stress_chart.setter
    def show_root_stress_chart(self, value: 'bool'):
        self.wrapped.ShowRootStressChart = bool(value) if value else False

    @property
    def edit_root_stress_legend(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'EditRootStressLegend' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EditRootStressLegend

    @property
    def show_contact_points(self) -> 'bool':
        '''bool: 'ShowContactPoints' is the original name of this property.'''

        return self.wrapped.ShowContactPoints

    @show_contact_points.setter
    def show_contact_points(self, value: 'bool'):
        self.wrapped.ShowContactPoints = bool(value) if value else False

    @property
    def gear_option(self) -> '_1031.DrawDefiningGearOrBoth':
        '''DrawDefiningGearOrBoth: 'GearOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearOption)
        return constructor.new(_1031.DrawDefiningGearOrBoth)(value) if value else None

    @gear_option.setter
    def gear_option(self, value: '_1031.DrawDefiningGearOrBoth'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearOption = value

    @property
    def contact_results(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ContactResultType':
        '''enum_with_selected_value.EnumWithSelectedValue_ContactResultType: 'ContactResults' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_ContactResultType)(self.wrapped.ContactResults) if self.wrapped.ContactResults else None

    @contact_results.setter
    def contact_results(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ContactResultType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ContactResultType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.ContactResults = value

    @property
    def root_stress_results_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressResultsType':
        '''enum_with_selected_value.EnumWithSelectedValue_StressResultsType: 'RootStressResultsType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_StressResultsType)(self.wrapped.RootStressResultsType) if self.wrapped.RootStressResultsType else None

    @root_stress_results_type.setter
    def root_stress_results_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressResultsType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_StressResultsType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressResultsType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.RootStressResultsType = value
