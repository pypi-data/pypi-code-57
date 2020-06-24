'''_3106.py

SynchroniserSleeveCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2025
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3876
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3105
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SynchroniserSleeveCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundModalAnalysis',)


class SynchroniserSleeveCompoundModalAnalysis(_3105.SynchroniserPartCompoundModalAnalysis):
    '''SynchroniserSleeveCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3876.SynchroniserSleeveModalAnalysis]':
        '''List[SynchroniserSleeveModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3876.SynchroniserSleeveModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3876.SynchroniserSleeveModalAnalysis]':
        '''List[SynchroniserSleeveModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3876.SynchroniserSleeveModalAnalysis))
        return value
