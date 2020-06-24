'''_4883.py

SynchroniserHalfCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2024
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4758
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _4884
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'SynchroniserHalfCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundSteadyStateSynchronousResponse',)


class SynchroniserHalfCompoundSteadyStateSynchronousResponse(_4884.SynchroniserPartCompoundSteadyStateSynchronousResponse):
    '''SynchroniserHalfCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2024.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4758.SynchroniserHalfSteadyStateSynchronousResponse]':
        '''List[SynchroniserHalfSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4758.SynchroniserHalfSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_4758.SynchroniserHalfSteadyStateSynchronousResponse]':
        '''List[SynchroniserHalfSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_4758.SynchroniserHalfSteadyStateSynchronousResponse))
        return value
