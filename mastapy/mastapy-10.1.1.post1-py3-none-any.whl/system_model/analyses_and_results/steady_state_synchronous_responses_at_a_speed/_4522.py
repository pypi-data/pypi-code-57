'''_4522.py

SynchroniserSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _1976
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2198
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4502
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'SynchroniserSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSteadyStateSynchronousResponseAtASpeed',)


class SynchroniserSteadyStateSynchronousResponseAtASpeed(_4502.SpecialisedAssemblySteadyStateSynchronousResponseAtASpeed):
    '''SynchroniserSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1976.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2198.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
