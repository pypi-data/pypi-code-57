'''_3267.py

ExternalCADModelCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1919
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3917
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3264
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ExternalCADModelCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundModalAnalysis',)


class ExternalCADModelCompoundModalAnalysis(_3264.ComponentCompoundModalAnalysis):
    '''ExternalCADModelCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3917.ExternalCADModelModalAnalysis]':
        '''List[ExternalCADModelModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3917.ExternalCADModelModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3917.ExternalCADModelModalAnalysis]':
        '''List[ExternalCADModelModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3917.ExternalCADModelModalAnalysis))
        return value
