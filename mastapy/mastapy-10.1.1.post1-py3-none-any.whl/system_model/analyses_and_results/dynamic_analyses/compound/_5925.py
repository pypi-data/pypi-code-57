'''_5925.py

BeltConnectionCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1832
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5802
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5977
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BeltConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundDynamicAnalysis',)


class BeltConnectionCompoundDynamicAnalysis(_5977.InterMountableComponentConnectionCompoundDynamicAnalysis):
    '''BeltConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5802.BeltConnectionDynamicAnalysis]':
        '''List[BeltConnectionDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5802.BeltConnectionDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_5802.BeltConnectionDynamicAnalysis]':
        '''List[BeltConnectionDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_5802.BeltConnectionDynamicAnalysis))
        return value
