'''_2746.py

CoaxialConnectionCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1761
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3645
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2751
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CoaxialConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionCompoundDynamicAnalysis',)


class CoaxialConnectionCompoundDynamicAnalysis(_2751.ShaftToMountableComponentConnectionCompoundDynamicAnalysis):
    '''CoaxialConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1761.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1761.CoaxialConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1761.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1761.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3645.CoaxialConnectionDynamicAnalysis]':
        '''List[CoaxialConnectionDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3645.CoaxialConnectionDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_3645.CoaxialConnectionDynamicAnalysis]':
        '''List[CoaxialConnectionDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_3645.CoaxialConnectionDynamicAnalysis))
        return value
