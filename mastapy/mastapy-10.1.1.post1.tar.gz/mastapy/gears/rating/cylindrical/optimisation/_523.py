'''_523.py

CylindricalGearSetRatingOptimisationHelper
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical.optimisation import (
    _524, _528, _527, _529,
    _525
)
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation', 'CylindricalGearSetRatingOptimisationHelper')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetRatingOptimisationHelper',)


class CylindricalGearSetRatingOptimisationHelper(_1.APIBase):
    '''CylindricalGearSetRatingOptimisationHelper

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetRatingOptimisationHelper.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def create_optimisation_report(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateOptimisationReport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateOptimisationReport

    @property
    def set_helix_angle_for_maximum_safety_factor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetHelixAngleForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetHelixAngleForMaximumSafetyFactor

    @property
    def set_profile_shift_coefficient_for_maximum_safety_factor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetProfileShiftCoefficientForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetProfileShiftCoefficientForMaximumSafetyFactor

    @property
    def set_normal_module_for_maximum_safety_factor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetNormalModuleForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetNormalModuleForMaximumSafetyFactor

    @property
    def set_pressure_angle_for_maximum_safety_factor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetPressureAngleForMaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetPressureAngleForMaximumSafetyFactor

    @property
    def set_face_widths_for_required_safety_factor(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetFaceWidthsForRequiredSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForRequiredSafetyFactor

    @property
    def calculate_optimisation_charts(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateOptimisationCharts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateOptimisationCharts

    @property
    def profile_shift_coefficient_optimisation_results(self) -> '_524.OptimisationResultsPair[_528.SafetyFactorOptimisationStepResultNumber]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultNumber]: 'ProfileShiftCoefficientOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_524.OptimisationResultsPair)[_528.SafetyFactorOptimisationStepResultNumber](self.wrapped.ProfileShiftCoefficientOptimisationResults) if self.wrapped.ProfileShiftCoefficientOptimisationResults else None

    @property
    def helix_angle_optimisation_results(self) -> '_524.OptimisationResultsPair[_527.SafetyFactorOptimisationStepResultAngle]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultAngle]: 'HelixAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_524.OptimisationResultsPair)[_527.SafetyFactorOptimisationStepResultAngle](self.wrapped.HelixAngleOptimisationResults) if self.wrapped.HelixAngleOptimisationResults else None

    @property
    def normal_module_optimisation_results(self) -> '_524.OptimisationResultsPair[_529.SafetyFactorOptimisationStepResultShortLength]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultShortLength]: 'NormalModuleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_524.OptimisationResultsPair)[_529.SafetyFactorOptimisationStepResultShortLength](self.wrapped.NormalModuleOptimisationResults) if self.wrapped.NormalModuleOptimisationResults else None

    @property
    def pressure_angle_optimisation_results(self) -> '_524.OptimisationResultsPair[_527.SafetyFactorOptimisationStepResultAngle]':
        '''OptimisationResultsPair[SafetyFactorOptimisationStepResultAngle]: 'PressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_524.OptimisationResultsPair)[_527.SafetyFactorOptimisationStepResultAngle](self.wrapped.PressureAngleOptimisationResults) if self.wrapped.PressureAngleOptimisationResults else None

    @property
    def all_normal_module_optimisation_results(self) -> 'List[_525.SafetyFactorOptimisationResults[_529.SafetyFactorOptimisationStepResultShortLength]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultShortLength]]: 'AllNormalModuleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllNormalModuleOptimisationResults, constructor.new(_525.SafetyFactorOptimisationResults)[_529.SafetyFactorOptimisationStepResultShortLength])
        return value

    @property
    def all_helix_angle_optimisation_results(self) -> 'List[_525.SafetyFactorOptimisationResults[_527.SafetyFactorOptimisationStepResultAngle]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'AllHelixAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllHelixAngleOptimisationResults, constructor.new(_525.SafetyFactorOptimisationResults)[_527.SafetyFactorOptimisationStepResultAngle])
        return value

    @property
    def all_normal_pressure_angle_optimisation_results(self) -> 'List[_525.SafetyFactorOptimisationResults[_527.SafetyFactorOptimisationStepResultAngle]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'AllNormalPressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllNormalPressureAngleOptimisationResults, constructor.new(_525.SafetyFactorOptimisationResults)[_527.SafetyFactorOptimisationStepResultAngle])
        return value

    @property
    def helix_angle_and_normal_pressure_angle_optimisation_results(self) -> 'List[_525.SafetyFactorOptimisationResults[_527.SafetyFactorOptimisationStepResultAngle]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'HelixAngleAndNormalPressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HelixAngleAndNormalPressureAngleOptimisationResults, constructor.new(_525.SafetyFactorOptimisationResults)[_527.SafetyFactorOptimisationStepResultAngle])
        return value

    @property
    def all_profile_shift_optimisation_results(self) -> 'List[_525.SafetyFactorOptimisationResults[_528.SafetyFactorOptimisationStepResultNumber]]':
        '''List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultNumber]]: 'AllProfileShiftOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllProfileShiftOptimisationResults, constructor.new(_525.SafetyFactorOptimisationResults)[_528.SafetyFactorOptimisationStepResultNumber])
        return value
