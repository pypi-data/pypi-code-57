'''_3357.py

TorqueConverterConnectionCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1830
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4316
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3355
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'TorqueConverterConnectionCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundSingleMeshWhineAnalysis',)


class TorqueConverterConnectionCompoundSingleMeshWhineAnalysis(_3355.CouplingConnectionCompoundSingleMeshWhineAnalysis):
    '''TorqueConverterConnectionCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4316.TorqueConverterConnectionSingleMeshWhineAnalysis]':
        '''List[TorqueConverterConnectionSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4316.TorqueConverterConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def connection_single_mesh_whine_analysis_load_cases(self) -> 'List[_4316.TorqueConverterConnectionSingleMeshWhineAnalysis]':
        '''List[TorqueConverterConnectionSingleMeshWhineAnalysis]: 'ConnectionSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSingleMeshWhineAnalysisLoadCases, constructor.new(_4316.TorqueConverterConnectionSingleMeshWhineAnalysis))
        return value
