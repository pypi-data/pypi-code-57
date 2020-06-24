'''_4843.py

OilSealCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _1929
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4726
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _4808
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'OilSealCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundSteadyStateSynchronousResponse',)


class OilSealCompoundSteadyStateSynchronousResponse(_4808.ConnectorCompoundSteadyStateSynchronousResponse):
    '''OilSealCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1929.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1929.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4726.OilSealSteadyStateSynchronousResponse]':
        '''List[OilSealSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4726.OilSealSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_4726.OilSealSteadyStateSynchronousResponse]':
        '''List[OilSealSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_4726.OilSealSteadyStateSynchronousResponse))
        return value
