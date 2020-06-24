'''_5399.py

UnbalancedMassCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1938
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5281
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5400
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'UnbalancedMassCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundModalAnalysesAtSpeeds',)


class UnbalancedMassCompoundModalAnalysesAtSpeeds(_5400.VirtualComponentCompoundModalAnalysesAtSpeeds):
    '''UnbalancedMassCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5281.UnbalancedMassModalAnalysesAtSpeeds]':
        '''List[UnbalancedMassModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5281.UnbalancedMassModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_5281.UnbalancedMassModalAnalysesAtSpeeds]':
        '''List[UnbalancedMassModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_5281.UnbalancedMassModalAnalysesAtSpeeds))
        return value
