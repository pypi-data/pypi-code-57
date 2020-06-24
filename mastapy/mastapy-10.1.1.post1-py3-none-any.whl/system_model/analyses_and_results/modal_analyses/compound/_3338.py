'''_3338.py

SpringDamperCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2036
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3870
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3330
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SpringDamperCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundModalAnalysis',)


class SpringDamperCompoundModalAnalysis(_3330.CouplingCompoundModalAnalysis):
    '''SpringDamperCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2036.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2036.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2036.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2036.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3870.SpringDamperModalAnalysis]':
        '''List[SpringDamperModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3870.SpringDamperModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3870.SpringDamperModalAnalysis]':
        '''List[SpringDamperModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3870.SpringDamperModalAnalysis))
        return value
