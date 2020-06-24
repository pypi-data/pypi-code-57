'''_5608.py

PlanetaryConnectionCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1848
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5486
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5620
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'PlanetaryConnectionCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundSingleMeshWhineAnalysis',)


class PlanetaryConnectionCompoundSingleMeshWhineAnalysis(_5620.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis):
    '''PlanetaryConnectionCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1848.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1848.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1848.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1848.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5486.PlanetaryConnectionSingleMeshWhineAnalysis]':
        '''List[PlanetaryConnectionSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5486.PlanetaryConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def connection_single_mesh_whine_analysis_load_cases(self) -> 'List[_5486.PlanetaryConnectionSingleMeshWhineAnalysis]':
        '''List[PlanetaryConnectionSingleMeshWhineAnalysis]: 'ConnectionSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSingleMeshWhineAnalysisLoadCases, constructor.new(_5486.PlanetaryConnectionSingleMeshWhineAnalysis))
        return value
