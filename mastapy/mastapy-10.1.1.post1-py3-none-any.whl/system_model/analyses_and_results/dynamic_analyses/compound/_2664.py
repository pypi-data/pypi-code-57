'''_2664.py

ExternalCADModelCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1919
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3681
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2661
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ExternalCADModelCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundDynamicAnalysis',)


class ExternalCADModelCompoundDynamicAnalysis(_2661.ComponentCompoundDynamicAnalysis):
    '''ExternalCADModelCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3681.ExternalCADModelDynamicAnalysis]':
        '''List[ExternalCADModelDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3681.ExternalCADModelDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_3681.ExternalCADModelDynamicAnalysis]':
        '''List[ExternalCADModelDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_3681.ExternalCADModelDynamicAnalysis))
        return value
