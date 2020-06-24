'''_387.py

CylindricalGearSetDesign
'''


from typing import List, Callable

from mastapy.gears.gear_designs.cylindrical import (
    _970, _993, _561, _1005,
    _1018, _1003, _537, _491,
    _983
)
from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.gears import _291
from mastapy.materials.efficiency import _278
from mastapy.gears.rating.cylindrical.iso6336 import _530
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1033
from mastapy.gears.manufacturing.cylindrical import _624
from mastapy.gears.rating.cylindrical import _398
from mastapy.gears.gear_designs import _385

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetDesign',)


class CylindricalGearSetDesign(_385.GearSetDesign):
    '''CylindricalGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def profile_shift_distribution_rule(self) -> '_970.AddendumModificationDistributionRule':
        '''AddendumModificationDistributionRule: 'ProfileShiftDistributionRule' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileShiftDistributionRule)
        return constructor.new(_970.AddendumModificationDistributionRule)(value) if value else None

    @profile_shift_distribution_rule.setter
    def profile_shift_distribution_rule(self, value: '_970.AddendumModificationDistributionRule'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileShiftDistributionRule = value

    @property
    def gear_tooth_thickness_reduction_allowance(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'GearToothThicknessReductionAllowance' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.GearToothThicknessReductionAllowance) if self.wrapped.GearToothThicknessReductionAllowance else None

    @gear_tooth_thickness_reduction_allowance.setter
    def gear_tooth_thickness_reduction_allowance(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.GearToothThicknessReductionAllowance = value

    @property
    def gear_tooth_thickness_tolerance(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'GearToothThicknessTolerance' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.GearToothThicknessTolerance) if self.wrapped.GearToothThicknessTolerance else None

    @gear_tooth_thickness_tolerance.setter
    def gear_tooth_thickness_tolerance(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.GearToothThicknessTolerance = value

    @property
    def coefficient_of_friction_calculation_method(self) -> 'overridable.Overridable_CoefficientOfFrictionCalculationMethod':
        '''overridable.Overridable_CoefficientOfFrictionCalculationMethod: 'CoefficientOfFrictionCalculationMethod' is the original name of this property.'''

        return constructor.new(overridable.Overridable_CoefficientOfFrictionCalculationMethod)(self.wrapped.CoefficientOfFrictionCalculationMethod) if self.wrapped.CoefficientOfFrictionCalculationMethod else None

    @coefficient_of_friction_calculation_method.setter
    def coefficient_of_friction_calculation_method(self, value: 'overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.TYPE
        enclosed_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.CoefficientOfFrictionCalculationMethod = value

    @property
    def efficiency_rating_method(self) -> '_278.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.EfficiencyRatingMethod)
        return constructor.new(_278.EfficiencyRatingMethod)(value) if value else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: '_278.EfficiencyRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def helical_gear_micro_geometry_option(self) -> '_530.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'HelicalGearMicroGeometryOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HelicalGearMicroGeometryOption)
        return constructor.new(_530.HelicalGearMicroGeometryOption)(value) if value else None

    @helical_gear_micro_geometry_option.setter
    def helical_gear_micro_geometry_option(self, value: '_530.HelicalGearMicroGeometryOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HelicalGearMicroGeometryOption = value

    @property
    def gear_fit_system(self) -> '_993.GearFitSystems':
        '''GearFitSystems: 'GearFitSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearFitSystem)
        return constructor.new(_993.GearFitSystems)(value) if value else None

    @gear_fit_system.setter
    def gear_fit_system(self, value: '_993.GearFitSystems'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearFitSystem = value

    @property
    def helix_angle(self) -> 'float':
        '''float: 'HelixAngle' is the original name of this property.'''

        return self.wrapped.HelixAngle

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def normal_module_maintain_transverse_profile(self) -> 'float':
        '''float: 'NormalModuleMaintainTransverseProfile' is the original name of this property.'''

        return self.wrapped.NormalModuleMaintainTransverseProfile

    @normal_module_maintain_transverse_profile.setter
    def normal_module_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.NormalModuleMaintainTransverseProfile = float(value) if value else 0.0

    @property
    def helix_angle_maintain_transverse_profile(self) -> 'float':
        '''float: 'HelixAngleMaintainTransverseProfile' is the original name of this property.'''

        return self.wrapped.HelixAngleMaintainTransverseProfile

    @helix_angle_maintain_transverse_profile.setter
    def helix_angle_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.HelixAngleMaintainTransverseProfile = float(value) if value else 0.0

    @property
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(self) -> 'float':
        '''float: 'RootGearProfileShiftCoefficientMaintainTipAndRootDiameters' is the original name of this property.'''

        return self.wrapped.RootGearProfileShiftCoefficientMaintainTipAndRootDiameters

    @root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters.setter
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(self, value: 'float'):
        self.wrapped.RootGearProfileShiftCoefficientMaintainTipAndRootDiameters = float(value) if value else 0.0

    @property
    def normal_pressure_angle_maintain_transverse_profile(self) -> 'float':
        '''float: 'NormalPressureAngleMaintainTransverseProfile' is the original name of this property.'''

        return self.wrapped.NormalPressureAngleMaintainTransverseProfile

    @normal_pressure_angle_maintain_transverse_profile.setter
    def normal_pressure_angle_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.NormalPressureAngleMaintainTransverseProfile = float(value) if value else 0.0

    @property
    def helix_angle_calculating_gear_teeth_numbers(self) -> 'float':
        '''float: 'HelixAngleCalculatingGearTeethNumbers' is the original name of this property.'''

        return self.wrapped.HelixAngleCalculatingGearTeethNumbers

    @helix_angle_calculating_gear_teeth_numbers.setter
    def helix_angle_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.HelixAngleCalculatingGearTeethNumbers = float(value) if value else 0.0

    @property
    def helix_angle_with_centre_distance_adjustment(self) -> 'float':
        '''float: 'HelixAngleWithCentreDistanceAdjustment' is the original name of this property.'''

        return self.wrapped.HelixAngleWithCentreDistanceAdjustment

    @helix_angle_with_centre_distance_adjustment.setter
    def helix_angle_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.HelixAngleWithCentreDistanceAdjustment = float(value) if value else 0.0

    @property
    def normal_pressure_angle(self) -> 'float':
        '''float: 'NormalPressureAngle' is the original name of this property.'''

        return self.wrapped.NormalPressureAngle

    @normal_pressure_angle.setter
    def normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalPressureAngle = float(value) if value else 0.0

    @property
    def normal_module(self) -> 'float':
        '''float: 'NormalModule' is the original name of this property.'''

        return self.wrapped.NormalModule

    @normal_module.setter
    def normal_module(self, value: 'float'):
        self.wrapped.NormalModule = float(value) if value else 0.0

    @property
    def normal_module_calculating_gear_teeth_numbers(self) -> 'float':
        '''float: 'NormalModuleCalculatingGearTeethNumbers' is the original name of this property.'''

        return self.wrapped.NormalModuleCalculatingGearTeethNumbers

    @normal_module_calculating_gear_teeth_numbers.setter
    def normal_module_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.NormalModuleCalculatingGearTeethNumbers = float(value) if value else 0.0

    @property
    def normal_module_with_centre_distance_adjustment(self) -> 'float':
        '''float: 'NormalModuleWithCentreDistanceAdjustment' is the original name of this property.'''

        return self.wrapped.NormalModuleWithCentreDistanceAdjustment

    @normal_module_with_centre_distance_adjustment.setter
    def normal_module_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.NormalModuleWithCentreDistanceAdjustment = float(value) if value else 0.0

    @property
    def diametral_pitch_per_inch(self) -> 'float':
        '''float: 'DiametralPitchPerInch' is the original name of this property.'''

        return self.wrapped.DiametralPitchPerInch

    @diametral_pitch_per_inch.setter
    def diametral_pitch_per_inch(self, value: 'float'):
        self.wrapped.DiametralPitchPerInch = float(value) if value else 0.0

    @property
    def transverse_pitch(self) -> 'float':
        '''float: 'TransversePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransversePitch

    @property
    def axial_pitch(self) -> 'float':
        '''float: 'AxialPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialPitch

    @property
    def transverse_module(self) -> 'float':
        '''float: 'TransverseModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseModule

    @property
    def base_helix_angle(self) -> 'float':
        '''float: 'BaseHelixAngle' is the original name of this property.'''

        return self.wrapped.BaseHelixAngle

    @base_helix_angle.setter
    def base_helix_angle(self, value: 'float'):
        self.wrapped.BaseHelixAngle = float(value) if value else 0.0

    @property
    def normal_pitch(self) -> 'float':
        '''float: 'NormalPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalPitch

    @property
    def normal_base_pitch(self) -> 'float':
        '''float: 'NormalBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalBasePitch

    @property
    def normal_base_pitch_set_by_changing_normal_module(self) -> 'float':
        '''float: 'NormalBasePitchSetByChangingNormalModule' is the original name of this property.'''

        return self.wrapped.NormalBasePitchSetByChangingNormalModule

    @normal_base_pitch_set_by_changing_normal_module.setter
    def normal_base_pitch_set_by_changing_normal_module(self, value: 'float'):
        self.wrapped.NormalBasePitchSetByChangingNormalModule = float(value) if value else 0.0

    @property
    def normal_base_pitch_set_by_changing_normal_pressure_angle(self) -> 'float':
        '''float: 'NormalBasePitchSetByChangingNormalPressureAngle' is the original name of this property.'''

        return self.wrapped.NormalBasePitchSetByChangingNormalPressureAngle

    @normal_base_pitch_set_by_changing_normal_pressure_angle.setter
    def normal_base_pitch_set_by_changing_normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalBasePitchSetByChangingNormalPressureAngle = float(value) if value else 0.0

    @property
    def transverse_base_pitch(self) -> 'float':
        '''float: 'TransverseBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseBasePitch

    @property
    def transverse_pressure_angle(self) -> 'float':
        '''float: 'TransversePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransversePressureAngle

    @property
    def transverse_pressure_angle_normal_pressure_angle(self) -> 'float':
        '''float: 'TransversePressureAngleNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransversePressureAngleNormalPressureAngle

    @property
    def all_gears_number_of_teeth(self) -> 'List[int]':
        '''List[int]: 'AllGearsNumberOfTeeth' is the original name of this property.'''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllGearsNumberOfTeeth, int)
        return value

    @all_gears_number_of_teeth.setter
    def all_gears_number_of_teeth(self, value: 'List[int]'):
        value = value if value else None
        value = conversion.mp_to_pn_objects_in_list(value)
        self.wrapped.AllGearsNumberOfTeeth = value

    @property
    def parameter_for_calculating_tooth_temperature(self) -> 'float':
        '''float: 'ParameterForCalculatingToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ParameterForCalculatingToothTemperature

    @property
    def centre_distance_editor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CentreDistanceEditor' is the original name of this property.'''

        return self.wrapped.CentreDistanceEditor

    @centre_distance_editor.setter
    def centre_distance_editor(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.CentreDistanceEditor = value

    @property
    def fe_model_for_tiff(self) -> 'str':
        '''str: 'FEModelForTIFF' is the original name of this property.'''

        return self.wrapped.FEModelForTIFF.SelectedItemName

    @fe_model_for_tiff.setter
    def fe_model_for_tiff(self, value: 'str'):
        self.wrapped.FEModelForTIFF.SetSelectedItem(str(value) if value else None)

    @property
    def minimum_axial_contact_ratio(self) -> 'float':
        '''float: 'MinimumAxialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumAxialContactRatio

    @property
    def minimum_transverse_contact_ratio(self) -> 'float':
        '''float: 'MinimumTransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTransverseContactRatio

    @property
    def minimum_total_contact_ratio(self) -> 'float':
        '''float: 'MinimumTotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTotalContactRatio

    @property
    def set_helix_angle_for_axial_contact_ratio(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetHelixAngleForAxialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetHelixAngleForAxialContactRatio

    @property
    def minimum_tip_thickness(self) -> 'float':
        '''float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTipThickness

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_1033.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1033.CylindricalGearSetMicroGeometry)(self.wrapped.CylindricalGearSetMicroGeometry) if self.wrapped.CylindricalGearSetMicroGeometry else None

    @property
    def scuffing(self) -> '_561.Scuffing':
        '''Scuffing: 'Scuffing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_561.Scuffing)(self.wrapped.Scuffing) if self.wrapped.Scuffing else None

    @property
    def micropitting(self) -> '_1005.Micropitting':
        '''Micropitting: 'Micropitting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1005.Micropitting)(self.wrapped.Micropitting) if self.wrapped.Micropitting else None

    @property
    def usage(self) -> '_1018.Usage':
        '''Usage: 'Usage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1018.Usage)(self.wrapped.Usage) if self.wrapped.Usage else None

    @property
    def ltca_settings(self) -> '_1003.LtcaSettings':
        '''LtcaSettings: 'LTCASettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1003.LtcaSettings)(self.wrapped.LTCASettings) if self.wrapped.LTCASettings else None

    @property
    def cylindrical_gear_set_manufacturing_configuration(self) -> '_624.CylindricalSetManufacturingConfig':
        '''CylindricalSetManufacturingConfig: 'CylindricalGearSetManufacturingConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_624.CylindricalSetManufacturingConfig)(self.wrapped.CylindricalGearSetManufacturingConfiguration) if self.wrapped.CylindricalGearSetManufacturingConfiguration else None

    @property
    def gears(self) -> 'List[_537.CylindricalGearDesign]':
        '''List[CylindricalGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_537.CylindricalGearDesign))
        return value

    @property
    def cylindrical_gears(self) -> 'List[_537.CylindricalGearDesign]':
        '''List[CylindricalGearDesign]: 'CylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGears, constructor.new(_537.CylindricalGearDesign))
        return value

    @property
    def cylindrical_meshes(self) -> 'List[_491.CylindricalGearMeshDesign]':
        '''List[CylindricalGearMeshDesign]: 'CylindricalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshes, constructor.new(_491.CylindricalGearMeshDesign))
        return value

    def try_make_valid(self):
        ''' 'TryMakeValid' is the original name of this method.'''

        self.wrapped.TryMakeValid()

    def clear_all_tooth_thickness_specifications(self):
        ''' 'ClearAllToothThicknessSpecifications' is the original name of this method.'''

        self.wrapped.ClearAllToothThicknessSpecifications()

    def create_optimiser(self, duty_cycle: '_398.CylindricalGearSetDutyCycleRating') -> '_983.CylindricalGearSetMacroGeometryOptimiser':
        ''' 'CreateOptimiser' is the original name of this method.

        Args:
            duty_cycle (mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating)

        Returns:
            mastapy.gears.gear_designs.cylindrical.CylindricalGearSetMacroGeometryOptimiser
        '''

        method_result = self.wrapped.CreateOptimiser(duty_cycle.wrapped if duty_cycle else None)
        return constructor.new(_983.CylindricalGearSetMacroGeometryOptimiser)(method_result) if method_result else None
