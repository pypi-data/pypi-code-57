'''_5924.py

BearingCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5801
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5952
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BearingCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundDynamicAnalysis',)


class BearingCompoundDynamicAnalysis(_5952.ConnectorCompoundDynamicAnalysis):
    '''BearingCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5801.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5801.BearingDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5801.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5801.BearingDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundDynamicAnalysis]':
        '''List[BearingCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundDynamicAnalysis))
        return value
