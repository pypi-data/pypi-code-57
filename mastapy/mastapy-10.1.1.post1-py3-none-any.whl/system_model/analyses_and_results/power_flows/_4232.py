'''_4232.py

StraightBevelGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2006
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2361
from mastapy.gears.rating.straight_bevel import _414
from mastapy.system_model.analyses_and_results.power_flows import _4210
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'StraightBevelGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearPowerFlow',)


class StraightBevelGearPowerFlow(_4210.BevelGearPowerFlow):
    '''StraightBevelGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2361.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2361.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_414.StraightBevelGearRating':
        '''StraightBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_414.StraightBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
