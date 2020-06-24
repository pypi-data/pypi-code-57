'''_2770.py

FaceGearSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.gears import _2067
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6113
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2774
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'FaceGearSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSteadyStateSynchronousResponseAtASpeed',)


class FaceGearSteadyStateSynchronousResponseAtASpeed(_2774.GearSteadyStateSynchronousResponseAtASpeed):
    '''FaceGearSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2067.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2067.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6113.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6113.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
