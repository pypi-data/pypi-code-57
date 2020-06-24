'''_3322.py

StraightBevelPlanetGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3317
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelPlanetGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearPowerFlow',)


class StraightBevelPlanetGearPowerFlow(_3317.StraightBevelDiffGearPowerFlow):
    '''StraightBevelPlanetGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2088.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
