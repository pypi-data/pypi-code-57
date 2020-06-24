'''_2495.py

BoltedJointSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2568
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'BoltedJointSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointSteadyStateSynchronousResponseOnAShaft',)


class BoltedJointSteadyStateSynchronousResponseOnAShaft(_2568.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft):
    '''BoltedJointSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1988.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6065.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6065.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
