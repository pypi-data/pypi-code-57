'''_5210.py

StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2085
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5208, _5209, _5127
from mastapy.system_model.analyses_and_results.mbd_analyses import _5080
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis',)


class StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis(_5127.BevelGearSetCompoundMultiBodyDynamicsAnalysis):
    '''StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2085.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2085.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2085.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2085.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5208.StraightBevelDiffGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearCompoundMultiBodyDynamicsAnalysis]: 'StraightBevelDiffGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5208.StraightBevelDiffGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5209.StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis]: 'StraightBevelDiffMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5209.StraightBevelDiffGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5080.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5080.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5080.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5080.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis))
        return value
