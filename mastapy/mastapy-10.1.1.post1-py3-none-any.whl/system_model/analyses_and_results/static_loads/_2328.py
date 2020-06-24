'''_2328.py

CylindricalGearSetLoadCase
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears import _291
from mastapy._internal.implicit import overridable
from mastapy.materials.efficiency import _277
from mastapy.system_model.analyses_and_results.static_loads import (
    _6287, _2326, _2244, _6239,
    _2334
)
from mastapy.system_model.part_model.gears import _1968
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1029
from mastapy.gears.gear_designs.cylindrical import _925
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetLoadCase',)


class CylindricalGearSetLoadCase(_2334.GearSetLoadCase):
    '''CylindricalGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def override_micro_geometry(self) -> 'bool':
        '''bool: 'OverrideMicroGeometry' is the original name of this property.'''

        return self.wrapped.OverrideMicroGeometry

    @override_micro_geometry.setter
    def override_micro_geometry(self, value: 'bool'):
        self.wrapped.OverrideMicroGeometry = bool(value) if value else False

    @property
    def coefficient_of_friction_calculation_method(self) -> '_291.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'CoefficientOfFrictionCalculationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CoefficientOfFrictionCalculationMethod)
        return constructor.new(_291.CoefficientOfFrictionCalculationMethod)(value) if value else None

    @coefficient_of_friction_calculation_method.setter
    def coefficient_of_friction_calculation_method(self, value: '_291.CoefficientOfFrictionCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoefficientOfFrictionCalculationMethod = value

    @property
    def efficiency_rating_method(self) -> 'overridable.Overridable_EfficiencyRatingMethod':
        '''overridable.Overridable_EfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property.'''

        return constructor.new(overridable.Overridable_EfficiencyRatingMethod)(self.wrapped.EfficiencyRatingMethod) if self.wrapped.EfficiencyRatingMethod else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: 'overridable.Overridable_EfficiencyRatingMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_EfficiencyRatingMethod.TYPE
        enclosed_type = overridable.Overridable_EfficiencyRatingMethod.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def use_design_coefficient_of_friction_calculation_method(self) -> 'bool':
        '''bool: 'UseDesignCoefficientOfFrictionCalculationMethod' is the original name of this property.'''

        return self.wrapped.UseDesignCoefficientOfFrictionCalculationMethod

    @use_design_coefficient_of_friction_calculation_method.setter
    def use_design_coefficient_of_friction_calculation_method(self, value: 'bool'):
        self.wrapped.UseDesignCoefficientOfFrictionCalculationMethod = bool(value) if value else False

    @property
    def use_design_default_ltca_settings(self) -> 'bool':
        '''bool: 'UseDesignDefaultLTCASettings' is the original name of this property.'''

        return self.wrapped.UseDesignDefaultLTCASettings

    @use_design_default_ltca_settings.setter
    def use_design_default_ltca_settings(self, value: 'bool'):
        self.wrapped.UseDesignDefaultLTCASettings = bool(value) if value else False

    @property
    def reset_micro_geometry(self) -> '_6287.ResetMicroGeometryOptions':
        '''ResetMicroGeometryOptions: 'ResetMicroGeometry' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ResetMicroGeometry)
        return constructor.new(_6287.ResetMicroGeometryOptions)(value) if value else None

    @reset_micro_geometry.setter
    def reset_micro_geometry(self, value: '_6287.ResetMicroGeometryOptions'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ResetMicroGeometry = value

    @property
    def boost_pressure(self) -> 'float':
        '''float: 'BoostPressure' is the original name of this property.'''

        return self.wrapped.BoostPressure

    @boost_pressure.setter
    def boost_pressure(self, value: 'float'):
        self.wrapped.BoostPressure = float(value) if value else 0.0

    @property
    def dynamic_load_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DynamicLoadFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DynamicLoadFactor) if self.wrapped.DynamicLoadFactor else None

    @dynamic_load_factor.setter
    def dynamic_load_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DynamicLoadFactor = value

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def overridden_micro_geometry(self) -> '_1029.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'OverriddenMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1029.CylindricalGearSetMicroGeometry)(self.wrapped.OverriddenMicroGeometry) if self.wrapped.OverriddenMicroGeometry else None

    @property
    def ltca(self) -> '_925.LTCALoadCaseModifiableSettings':
        '''LTCALoadCaseModifiableSettings: 'LTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_925.LTCALoadCaseModifiableSettings)(self.wrapped.LTCA) if self.wrapped.LTCA else None

    @property
    def cylindrical_gears_load_case(self) -> 'List[_2326.CylindricalGearLoadCase]':
        '''List[CylindricalGearLoadCase]: 'CylindricalGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsLoadCase, constructor.new(_2326.CylindricalGearLoadCase))
        return value

    @property
    def cylindrical_meshes_load_case(self) -> 'List[_2244.CylindricalGearMeshLoadCase]':
        '''List[CylindricalGearMeshLoadCase]: 'CylindricalMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesLoadCase, constructor.new(_2244.CylindricalGearMeshLoadCase))
        return value

    def get_harmonic_load_data_for_import(self) -> '_6239.CylindricalGearSetHarmonicLoadData':
        ''' 'GetHarmonicLoadDataForImport' is the original name of this method.

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetHarmonicLoadData
        '''

        method_result = self.wrapped.GetHarmonicLoadDataForImport()
        return constructor.new(_6239.CylindricalGearSetHarmonicLoadData)(method_result) if method_result else None
