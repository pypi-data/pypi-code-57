'''_3022.py

HypoidGearSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.gears import _2073
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6133
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2968
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'HypoidGearSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSteadyStateSynchronousResponse',)


class HypoidGearSteadyStateSynchronousResponse(_2968.AGMAGleasonConicalGearSteadyStateSynchronousResponse):
    '''HypoidGearSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2073.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2073.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6133.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6133.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
