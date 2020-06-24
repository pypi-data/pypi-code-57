'''_4792.py

BoltedJointCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _1911
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4670
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _4859
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'BoltedJointCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundSteadyStateSynchronousResponse',)


class BoltedJointCompoundSteadyStateSynchronousResponse(_4859.SpecialisedAssemblyCompoundSteadyStateSynchronousResponse):
    '''BoltedJointCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4670.BoltedJointSteadyStateSynchronousResponse]':
        '''List[BoltedJointSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4670.BoltedJointSteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_4670.BoltedJointSteadyStateSynchronousResponse]':
        '''List[BoltedJointSteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_4670.BoltedJointSteadyStateSynchronousResponse))
        return value
