'''_45.py

ShaftSectionEndDamageResults
'''


from typing import List

from mastapy.nodal_analysis import _72
from mastapy._internal import constructor, conversion
from mastapy.shafts import (
    _39, _69, _40, _54
)
from mastapy.materials import _74
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_SECTION_END_DAMAGE_RESULTS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSectionEndDamageResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSectionEndDamageResults',)


class ShaftSectionEndDamageResults(_1.APIBase):
    '''ShaftSectionEndDamageResults

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SECTION_END_DAMAGE_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSectionEndDamageResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def section_end(self) -> '_72.SectionEnd':
        '''SectionEnd: 'SectionEnd' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.SectionEnd)
        return constructor.new(_72.SectionEnd)(value) if value else None

    @property
    def offset(self) -> 'float':
        '''float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Offset

    @property
    def outer_radius_to_achieve_shaft_fatigue_safety_factor_requirement(self) -> 'float':
        '''float: 'OuterRadiusToAchieveShaftFatigueSafetyFactorRequirement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRadiusToAchieveShaftFatigueSafetyFactorRequirement

    @property
    def outer_diameter_to_achieve_fatigue_safety_factor_requirement(self) -> 'float':
        '''float: 'OuterDiameterToAchieveFatigueSafetyFactorRequirement' is the original name of this property.'''

        return self.wrapped.OuterDiameterToAchieveFatigueSafetyFactorRequirement

    @outer_diameter_to_achieve_fatigue_safety_factor_requirement.setter
    def outer_diameter_to_achieve_fatigue_safety_factor_requirement(self, value: 'float'):
        self.wrapped.OuterDiameterToAchieveFatigueSafetyFactorRequirement = float(value) if value else 0.0

    @property
    def displacement_radial_magnitude(self) -> 'float':
        '''float: 'DisplacementRadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisplacementRadialMagnitude

    @property
    def displacement_radial_tilt_magnitude(self) -> 'float':
        '''float: 'DisplacementRadialTiltMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisplacementRadialTiltMagnitude

    @property
    def displacement_axial(self) -> 'float':
        '''float: 'DisplacementAxial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisplacementAxial

    @property
    def displacement_twist(self) -> 'float':
        '''float: 'DisplacementTwist' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisplacementTwist

    @property
    def force_axial(self) -> 'float':
        '''float: 'ForceAxial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceAxial

    @property
    def force_torque(self) -> 'float':
        '''float: 'ForceTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceTorque

    @property
    def force_radial_magnitude(self) -> 'float':
        '''float: 'ForceRadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceRadialMagnitude

    @property
    def static_safety_factor(self) -> 'float':
        '''float: 'StaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticSafetyFactor

    @property
    def fatigue_safety_factor(self) -> 'float':
        '''float: 'FatigueSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FatigueSafetyFactor

    @property
    def fatigue_damage(self) -> 'float':
        '''float: 'FatigueDamage' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FatigueDamage

    @property
    def fatigue_safety_factor_for_infinite_life(self) -> 'float':
        '''float: 'FatigueSafetyFactorForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FatigueSafetyFactorForInfiniteLife

    @property
    def shaft_reliability(self) -> 'float':
        '''float: 'ShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftReliability

    @property
    def reliability_for_infinite_life(self) -> 'float':
        '''float: 'ReliabilityForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReliabilityForInfiniteLife

    @property
    def total_number_of_cycles(self) -> 'float':
        '''float: 'TotalNumberOfCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalNumberOfCycles

    @property
    def equivalent_alternating_stress(self) -> 'float':
        '''float: 'EquivalentAlternatingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquivalentAlternatingStress

    @property
    def stress_concentration_factors(self) -> '_39.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'StressConcentrationFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_39.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.StressConcentrationFactors) if self.wrapped.StressConcentrationFactors else None

    @property
    def sn_curve(self) -> '_74.SNCurve':
        '''SNCurve: 'SNCurve' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_74.SNCurve)(self.wrapped.SNCurve) if self.wrapped.SNCurve else None

    @property
    def din743201212_alternate_strength(self) -> '_69.StressMeasurementShaftAxialBendingTorsionalComponentValues':
        '''StressMeasurementShaftAxialBendingTorsionalComponentValues: 'DIN743201212AlternateStrength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_69.StressMeasurementShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212AlternateStrength) if self.wrapped.DIN743201212AlternateStrength else None

    @property
    def din743201212_yielding_strength(self) -> '_69.StressMeasurementShaftAxialBendingTorsionalComponentValues':
        '''StressMeasurementShaftAxialBendingTorsionalComponentValues: 'DIN743201212YieldingStrength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_69.StressMeasurementShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212YieldingStrength) if self.wrapped.DIN743201212YieldingStrength else None

    @property
    def din743201212_influence_factor_for_mean_stress_sensitivity(self) -> '_39.ShaftAxialBendingTorsionalComponentValues':
        '''ShaftAxialBendingTorsionalComponentValues: 'DIN743201212InfluenceFactorForMeanStressSensitivity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_39.ShaftAxialBendingTorsionalComponentValues)(self.wrapped.DIN743201212InfluenceFactorForMeanStressSensitivity) if self.wrapped.DIN743201212InfluenceFactorForMeanStressSensitivity else None

    @property
    def fkm_guideline_6th_edition_2012_cyclic_degree_of_utilization_for_finite_life(self) -> '_40.ShaftAxialBendingXBendingYTorsionalComponentValues':
        '''ShaftAxialBendingXBendingYTorsionalComponentValues: 'FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForFiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_40.ShaftAxialBendingXBendingYTorsionalComponentValues)(self.wrapped.FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForFiniteLife) if self.wrapped.FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForFiniteLife else None

    @property
    def fkm_guideline_6th_edition_2012_cyclic_degree_of_utilization_for_infinite_life(self) -> '_40.ShaftAxialBendingXBendingYTorsionalComponentValues':
        '''ShaftAxialBendingXBendingYTorsionalComponentValues: 'FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_40.ShaftAxialBendingXBendingYTorsionalComponentValues)(self.wrapped.FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForInfiniteLife) if self.wrapped.FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForInfiniteLife else None

    @property
    def sn_curve_axial(self) -> '_74.SNCurve':
        '''SNCurve: 'SNCurveAxial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_74.SNCurve)(self.wrapped.SNCurveAxial) if self.wrapped.SNCurveAxial else None

    @property
    def sn_curve_bending_x(self) -> '_74.SNCurve':
        '''SNCurve: 'SNCurveBendingX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_74.SNCurve)(self.wrapped.SNCurveBendingX) if self.wrapped.SNCurveBendingX else None

    @property
    def sn_curve_bending_y(self) -> '_74.SNCurve':
        '''SNCurve: 'SNCurveBendingY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_74.SNCurve)(self.wrapped.SNCurveBendingY) if self.wrapped.SNCurveBendingY else None

    @property
    def sn_curve_torsional(self) -> '_74.SNCurve':
        '''SNCurve: 'SNCurveTorsional' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_74.SNCurve)(self.wrapped.SNCurveTorsional) if self.wrapped.SNCurveTorsional else None

    @property
    def stress_cycles(self) -> 'List[_54.ShaftPointStressCycleReporting]':
        '''List[ShaftPointStressCycleReporting]: 'StressCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StressCycles, constructor.new(_54.ShaftPointStressCycleReporting))
        return value

    @property
    def din743201212_yielding_amplitude(self) -> 'List[_69.StressMeasurementShaftAxialBendingTorsionalComponentValues]':
        '''List[StressMeasurementShaftAxialBendingTorsionalComponentValues]: 'DIN743201212YieldingAmplitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DIN743201212YieldingAmplitude, constructor.new(_69.StressMeasurementShaftAxialBendingTorsionalComponentValues))
        return value
