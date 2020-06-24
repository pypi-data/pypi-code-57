'''_5213.py

StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2087
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5211, _5212, _5127
from mastapy.system_model.analyses_and_results.mbd_analyses import _5083
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis',)


class StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis(_5127.BevelGearSetCompoundMultiBodyDynamicsAnalysis):
    '''StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2087.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2087.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5211.StraightBevelGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearCompoundMultiBodyDynamicsAnalysis]: 'StraightBevelGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5211.StraightBevelGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5212.StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis]: 'StraightBevelMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5212.StraightBevelGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5083.StraightBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5083.StraightBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5083.StraightBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5083.StraightBevelGearSetMultiBodyDynamicsAnalysis))
        return value
