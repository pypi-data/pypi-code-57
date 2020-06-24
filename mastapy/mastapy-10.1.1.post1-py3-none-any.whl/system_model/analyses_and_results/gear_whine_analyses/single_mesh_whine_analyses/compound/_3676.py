'''_3676.py

WormGearCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2010
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4325
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3657
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'WormGearCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearCompoundSingleMeshWhineAnalysis',)


class WormGearCompoundSingleMeshWhineAnalysis(_3657.GearCompoundSingleMeshWhineAnalysis):
    '''WormGearCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2010.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2010.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4325.WormGearSingleMeshWhineAnalysis]':
        '''List[WormGearSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4325.WormGearSingleMeshWhineAnalysis))
        return value

    @property
    def component_single_mesh_whine_analysis_load_cases(self) -> 'List[_4325.WormGearSingleMeshWhineAnalysis]':
        '''List[WormGearSingleMeshWhineAnalysis]: 'ComponentSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSingleMeshWhineAnalysisLoadCases, constructor.new(_4325.WormGearSingleMeshWhineAnalysis))
        return value
