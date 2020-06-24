'''_3311.py

SpiralBevelGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2082
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6178
from mastapy.gears.rating.spiral_bevel import _205
from mastapy.system_model.analyses_and_results.power_flows import _3231
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SpiralBevelGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearPowerFlow',)


class SpiralBevelGearPowerFlow(_3231.BevelGearPowerFlow):
    '''SpiralBevelGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2082.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2082.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6178.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6178.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_205.SpiralBevelGearRating':
        '''SpiralBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_205.SpiralBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
