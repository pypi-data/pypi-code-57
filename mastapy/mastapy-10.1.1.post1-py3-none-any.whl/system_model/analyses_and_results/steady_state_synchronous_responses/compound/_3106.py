'''_3106.py

BoltCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2982
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3112
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'BoltCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundSteadyStateSynchronousResponse',)


class BoltCompoundSteadyStateSynchronousResponse(_3112.ComponentCompoundSteadyStateSynchronousResponse):
    '''BoltCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1987.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2982.BoltSteadyStateSynchronousResponse]':
        '''List[BoltSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2982.BoltSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_2982.BoltSteadyStateSynchronousResponse]':
        '''List[BoltSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_2982.BoltSteadyStateSynchronousResponse))
        return value
