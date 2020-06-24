'''_5382.py

SpringDamperHalfCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2019
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5262
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5326
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'SpringDamperHalfCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfCompoundModalAnalysesAtSpeeds',)


class SpringDamperHalfCompoundModalAnalysesAtSpeeds(_5326.CouplingHalfCompoundModalAnalysesAtSpeeds):
    '''SpringDamperHalfCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5262.SpringDamperHalfModalAnalysesAtSpeeds]':
        '''List[SpringDamperHalfModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5262.SpringDamperHalfModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_5262.SpringDamperHalfModalAnalysesAtSpeeds]':
        '''List[SpringDamperHalfModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_5262.SpringDamperHalfModalAnalysesAtSpeeds))
        return value
