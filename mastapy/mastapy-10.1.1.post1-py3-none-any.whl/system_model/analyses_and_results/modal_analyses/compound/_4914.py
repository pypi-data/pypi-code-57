'''_4914.py

MassDiscCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2004
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4770
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4959
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'MassDiscCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundModalAnalysis',)


class MassDiscCompoundModalAnalysis(_4959.VirtualComponentCompoundModalAnalysis):
    '''MassDiscCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2004.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4770.MassDiscModalAnalysis]':
        '''List[MassDiscModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4770.MassDiscModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4770.MassDiscModalAnalysis]':
        '''List[MassDiscModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4770.MassDiscModalAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundModalAnalysis]':
        '''List[MassDiscCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundModalAnalysis))
        return value
