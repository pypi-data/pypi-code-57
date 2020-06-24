'''_4393.py

ImportedFEComponentCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2001
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4271
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4336
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ImportedFEComponentCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundModalAnalysisAtAStiffness',)


class ImportedFEComponentCompoundModalAnalysisAtAStiffness(_4336.AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness):
    '''ImportedFEComponentCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4271.ImportedFEComponentModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4271.ImportedFEComponentModalAnalysisAtAStiffness))
        return value

    @property
    def component_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4271.ImportedFEComponentModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentModalAnalysisAtAStiffness]: 'ComponentModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtAStiffnessLoadCases, constructor.new(_4271.ImportedFEComponentModalAnalysisAtAStiffness))
        return value

    @property
    def planetaries(self) -> 'List[ImportedFEComponentCompoundModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentCompoundModalAnalysisAtAStiffness))
        return value
