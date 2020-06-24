'''_40.py

SimpleShaftDefinition
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.shafts import (
    _24, _39, _29, _9,
    _32, _22, _38, _14
)
from mastapy.utility.databases import _1342

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_SIMPLE_SHAFT_DEFINITION = python_net_import('SMT.MastaAPI.Shafts', 'SimpleShaftDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('SimpleShaftDefinition',)


class SimpleShaftDefinition(_1342.NamedDatabaseItem):
    '''SimpleShaftDefinition

    This is a mastapy class.
    '''

    TYPE = _SIMPLE_SHAFT_DEFINITION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SimpleShaftDefinition.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def design_name(self) -> 'str':
        '''str: 'DesignName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DesignName

    @property
    def add_radial_hole(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddRadialHole' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddRadialHole

    @property
    def add_radial_hole_for_context_menu(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddRadialHoleForContextMenu' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddRadialHoleForContextMenu

    @property
    def add_groove(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddGroove' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddGroove

    @property
    def add_groove_for_context_menu(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddGrooveForContextMenu' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddGrooveForContextMenu

    @property
    def add_generic_stress_concentration_factor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddGenericStressConcentrationFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddGenericStressConcentrationFactor

    @property
    def add_generic_stress_concentration_factor_for_context_menu(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddGenericStressConcentrationFactorForContextMenu' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddGenericStressConcentrationFactorForContextMenu

    @property
    def add_surface_finish_section(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddSurfaceFinishSection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSurfaceFinishSection

    @property
    def add_surface_finish_section_for_context_menu(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddSurfaceFinishSectionForContextMenu' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSurfaceFinishSectionForContextMenu

    @property
    def material(self) -> 'str':
        '''str: 'Material' is the original name of this property.'''

        return self.wrapped.Material.SelectedItemName

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else None)

    @property
    def default_fillet_radius(self) -> 'float':
        '''float: 'DefaultFilletRadius' is the original name of this property.'''

        return self.wrapped.DefaultFilletRadius

    @default_fillet_radius.setter
    def default_fillet_radius(self, value: 'float'):
        self.wrapped.DefaultFilletRadius = float(value) if value else 0.0

    @property
    def surface_treatment_factor(self) -> 'float':
        '''float: 'SurfaceTreatmentFactor' is the original name of this property.'''

        return self.wrapped.SurfaceTreatmentFactor

    @surface_treatment_factor.setter
    def surface_treatment_factor(self, value: 'float'):
        self.wrapped.SurfaceTreatmentFactor = float(value) if value else 0.0

    @property
    def factor_for_gjl_material(self) -> 'float':
        '''float: 'FactorForGJLMaterial' is the original name of this property.'''

        return self.wrapped.FactorForGJLMaterial

    @factor_for_gjl_material.setter
    def factor_for_gjl_material(self, value: 'float'):
        self.wrapped.FactorForGJLMaterial = float(value) if value else 0.0

    @property
    def report_shaft_fatigue_warnings(self) -> 'bool':
        '''bool: 'ReportShaftFatigueWarnings' is the original name of this property.'''

        return self.wrapped.ReportShaftFatigueWarnings

    @report_shaft_fatigue_warnings.setter
    def report_shaft_fatigue_warnings(self, value: 'bool'):
        self.wrapped.ReportShaftFatigueWarnings = bool(value) if value else False

    @property
    def shaft_material(self) -> '_24.ShaftMaterial':
        '''ShaftMaterial: 'ShaftMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_24.ShaftMaterial)(self.wrapped.ShaftMaterial) if self.wrapped.ShaftMaterial else None

    @property
    def default_surface_roughness(self) -> '_39.ShaftSurfaceRoughness':
        '''ShaftSurfaceRoughness: 'DefaultSurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_39.ShaftSurfaceRoughness)(self.wrapped.DefaultSurfaceRoughness) if self.wrapped.DefaultSurfaceRoughness else None

    @property
    def outer_profile(self) -> '_29.ShaftProfile':
        '''ShaftProfile: 'OuterProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_29.ShaftProfile)(self.wrapped.OuterProfile) if self.wrapped.OuterProfile else None

    @property
    def inner_profile(self) -> '_29.ShaftProfile':
        '''ShaftProfile: 'InnerProfile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_29.ShaftProfile)(self.wrapped.InnerProfile) if self.wrapped.InnerProfile else None

    @property
    def design_shaft_sections(self) -> 'List[_9.DesignShaftSection]':
        '''List[DesignShaftSection]: 'DesignShaftSections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignShaftSections, constructor.new(_9.DesignShaftSection))
        return value

    @property
    def radial_holes(self) -> 'List[_32.ShaftRadialHole]':
        '''List[ShaftRadialHole]: 'RadialHoles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RadialHoles, constructor.new(_32.ShaftRadialHole))
        return value

    @property
    def grooves(self) -> 'List[_22.ShaftGroove]':
        '''List[ShaftGroove]: 'Grooves' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Grooves, constructor.new(_22.ShaftGroove))
        return value

    @property
    def surface_finish_sections(self) -> 'List[_38.ShaftSurfaceFinishSection]':
        '''List[ShaftSurfaceFinishSection]: 'SurfaceFinishSections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SurfaceFinishSections, constructor.new(_38.ShaftSurfaceFinishSection))
        return value

    @property
    def generic_stress_concentration_factors(self) -> 'List[_14.GenericStressConcentrationFactor]':
        '''List[GenericStressConcentrationFactor]: 'GenericStressConcentrationFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GenericStressConcentrationFactors, constructor.new(_14.GenericStressConcentrationFactor))
        return value
