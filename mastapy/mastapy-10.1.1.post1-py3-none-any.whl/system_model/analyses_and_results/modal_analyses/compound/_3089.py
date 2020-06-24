'''_3089.py

ClutchCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1988
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3859
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3093
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ClutchCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundModalAnalysis',)


class ClutchCompoundModalAnalysis(_3093.CouplingCompoundModalAnalysis):
    '''ClutchCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1988.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1988.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3859.ClutchModalAnalysis]':
        '''List[ClutchModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3859.ClutchModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3859.ClutchModalAnalysis]':
        '''List[ClutchModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3859.ClutchModalAnalysis))
        return value
