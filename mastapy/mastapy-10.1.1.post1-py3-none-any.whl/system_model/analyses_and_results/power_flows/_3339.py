'''_3339.py

ZerolBevelGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2092
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6212
from mastapy.gears.rating.zerol_bevel import _172
from mastapy.system_model.analyses_and_results.power_flows import _3231
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ZerolBevelGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearPowerFlow',)


class ZerolBevelGearPowerFlow(_3231.BevelGearPowerFlow):
    '''ZerolBevelGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2092.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6212.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6212.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_172.ZerolBevelGearRating':
        '''ZerolBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_172.ZerolBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
