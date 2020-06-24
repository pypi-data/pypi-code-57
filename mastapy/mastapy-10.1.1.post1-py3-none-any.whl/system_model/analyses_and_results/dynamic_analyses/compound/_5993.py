'''_5993.py

PartToPartShearCouplingConnectionCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1900
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5871
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5954
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PartToPartShearCouplingConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionCompoundDynamicAnalysis',)


class PartToPartShearCouplingConnectionCompoundDynamicAnalysis(_5954.CouplingConnectionCompoundDynamicAnalysis):
    '''PartToPartShearCouplingConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1900.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1900.PartToPartShearCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1900.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1900.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5871.PartToPartShearCouplingConnectionDynamicAnalysis]':
        '''List[PartToPartShearCouplingConnectionDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5871.PartToPartShearCouplingConnectionDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_5871.PartToPartShearCouplingConnectionDynamicAnalysis]':
        '''List[PartToPartShearCouplingConnectionDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_5871.PartToPartShearCouplingConnectionDynamicAnalysis))
        return value
