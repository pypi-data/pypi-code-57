'''_3690.py

ShaftHubConnectionCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4221
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3620
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ShaftHubConnectionCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundSingleMeshWhineAnalysis',)


class ShaftHubConnectionCompoundSingleMeshWhineAnalysis(_3620.ConnectorCompoundSingleMeshWhineAnalysis):
    '''ShaftHubConnectionCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2028.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4221.ShaftHubConnectionSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4221.ShaftHubConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def component_single_mesh_whine_analysis_load_cases(self) -> 'List[_4221.ShaftHubConnectionSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionSingleMeshWhineAnalysis]: 'ComponentSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSingleMeshWhineAnalysisLoadCases, constructor.new(_4221.ShaftHubConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundSingleMeshWhineAnalysis))
        return value
