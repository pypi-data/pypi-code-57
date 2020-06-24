'''_3071.py

StraightBevelPlanetGearSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3067
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'StraightBevelPlanetGearSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearSteadyStateSynchronousResponse',)


class StraightBevelPlanetGearSteadyStateSynchronousResponse(_3067.StraightBevelDiffGearSteadyStateSynchronousResponse):
    '''StraightBevelPlanetGearSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2088.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
