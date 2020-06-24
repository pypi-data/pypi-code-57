'''_4434.py

ClutchSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2173
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _4450
from mastapy._internal.python_net import python_net_import

_CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'ClutchSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchSteadyStateSynchronousResponseAtASpeed',)


class ClutchSteadyStateSynchronousResponseAtASpeed(_4450.CouplingSteadyStateSynchronousResponseAtASpeed):
    '''ClutchSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1988.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2173.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
