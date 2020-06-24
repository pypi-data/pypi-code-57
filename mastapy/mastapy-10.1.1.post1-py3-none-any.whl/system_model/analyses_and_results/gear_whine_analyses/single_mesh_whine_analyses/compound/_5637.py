'''_5637.py

SynchroniserHalfCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2137
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5515
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5638
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'SynchroniserHalfCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundSingleMeshWhineAnalysis',)


class SynchroniserHalfCompoundSingleMeshWhineAnalysis(_5638.SynchroniserPartCompoundSingleMeshWhineAnalysis):
    '''SynchroniserHalfCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5515.SynchroniserHalfSingleMeshWhineAnalysis]':
        '''List[SynchroniserHalfSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5515.SynchroniserHalfSingleMeshWhineAnalysis))
        return value

    @property
    def component_single_mesh_whine_analysis_load_cases(self) -> 'List[_5515.SynchroniserHalfSingleMeshWhineAnalysis]':
        '''List[SynchroniserHalfSingleMeshWhineAnalysis]: 'ComponentSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSingleMeshWhineAnalysisLoadCases, constructor.new(_5515.SynchroniserHalfSingleMeshWhineAnalysis))
        return value
