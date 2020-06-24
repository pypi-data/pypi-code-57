'''_4757.py

StraightBevelSunGearSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _4752
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'StraightBevelSunGearSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearSteadyStateSynchronousResponse',)


class StraightBevelSunGearSteadyStateSynchronousResponse(_4752.StraightBevelDiffGearSteadyStateSynchronousResponse):
    '''StraightBevelSunGearSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
