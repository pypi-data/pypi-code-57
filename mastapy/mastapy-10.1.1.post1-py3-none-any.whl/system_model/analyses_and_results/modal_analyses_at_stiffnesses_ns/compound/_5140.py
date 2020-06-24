'''_5140.py

SpringDamperHalfCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2019
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5021
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5084
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'SpringDamperHalfCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundModalAnalysesAtStiffnesses',)


class SpringDamperHalfCompoundModalAnalysesAtStiffnesses(_5084.CouplingHalfCompoundModalAnalysesAtStiffnesses):
    '''SpringDamperHalfCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5021.SpringDamperHalfModalAnalysesAtStiffnesses]':
        '''List[SpringDamperHalfModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5021.SpringDamperHalfModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_5021.SpringDamperHalfModalAnalysesAtStiffnesses]':
        '''List[SpringDamperHalfModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_5021.SpringDamperHalfModalAnalysesAtStiffnesses))
        return value
