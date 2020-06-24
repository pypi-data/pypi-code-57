'''_4973.py

BearingMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1985
from mastapy.system_model.analyses_and_results.static_loads import _6054
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5107
from mastapy.system_model.analyses_and_results.mbd_analyses import _5003
from mastapy._internal.python_net import python_net_import

_BEARING_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BearingMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMultiBodyDynamicsAnalysis',)


class BearingMultiBodyDynamicsAnalysis(_5003.ConnectorMultiBodyDynamicsAnalysis):
    '''BearingMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def basic_rating_life_damage_rate(self) -> 'float':
        '''float: 'BasicRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BasicRatingLifeDamageRate

    @property
    def basic_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'BasicRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BasicRatingLifeDamageDuringAnalysis

    @property
    def modified_rating_life_damage_rate(self) -> 'float':
        '''float: 'ModifiedRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModifiedRatingLifeDamageRate

    @property
    def modified_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'ModifiedRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModifiedRatingLifeDamageDuringAnalysis

    @property
    def basic_reference_rating_life_damage_rate(self) -> 'float':
        '''float: 'BasicReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BasicReferenceRatingLifeDamageRate

    @property
    def basic_reference_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'BasicReferenceRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BasicReferenceRatingLifeDamageDuringAnalysis

    @property
    def modified_reference_rating_life_damage_rate(self) -> 'float':
        '''float: 'ModifiedReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModifiedReferenceRatingLifeDamageRate

    @property
    def modified_reference_rating_life_damage_during_analysis(self) -> 'float':
        '''float: 'ModifiedReferenceRatingLifeDamageDuringAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModifiedReferenceRatingLifeDamageDuringAnalysis

    @property
    def iso762006_safety_factor_at_current_time(self) -> 'float':
        '''float: 'ISO762006SafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO762006SafetyFactorAtCurrentTime

    @property
    def iso762006_safety_factor(self) -> 'float':
        '''float: 'ISO762006SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO762006SafetyFactor

    @property
    def maximum_static_contact_stress_inner_safety_factor_at_current_time(self) -> 'float':
        '''float: 'MaximumStaticContactStressInnerSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressInnerSafetyFactorAtCurrentTime

    @property
    def maximum_static_contact_stress_inner_safety_factor(self) -> 'float':
        '''float: 'MaximumStaticContactStressInnerSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressInnerSafetyFactor

    @property
    def maximum_static_contact_stress_outer_safety_factor_at_current_time(self) -> 'float':
        '''float: 'MaximumStaticContactStressOuterSafetyFactorAtCurrentTime' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressOuterSafetyFactorAtCurrentTime

    @property
    def maximum_static_contact_stress_outer_safety_factor(self) -> 'float':
        '''float: 'MaximumStaticContactStressOuterSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumStaticContactStressOuterSafetyFactor

    @property
    def component_design(self) -> '_1985.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6054.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6054.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def peak_dynamic_force(self) -> '_5107.DynamicForceVector3DResult':
        '''DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5107.DynamicForceVector3DResult)(self.wrapped.PeakDynamicForce) if self.wrapped.PeakDynamicForce else None

    @property
    def planetaries(self) -> 'List[BearingMultiBodyDynamicsAnalysis]':
        '''List[BearingMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingMultiBodyDynamicsAnalysis))
        return value
