'''_2542.py

MassDiscCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1926
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3686
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2553
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'MassDiscCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundDynamicAnalysis',)


class MassDiscCompoundDynamicAnalysis(_2553.VirtualComponentCompoundDynamicAnalysis):
    '''MassDiscCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1926.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1926.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3686.MassDiscDynamicAnalysis]':
        '''List[MassDiscDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3686.MassDiscDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_3686.MassDiscDynamicAnalysis]':
        '''List[MassDiscDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_3686.MassDiscDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundDynamicAnalysis]':
        '''List[MassDiscCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundDynamicAnalysis))
        return value
