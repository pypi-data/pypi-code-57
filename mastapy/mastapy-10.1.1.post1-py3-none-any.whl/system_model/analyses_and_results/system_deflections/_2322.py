'''_2322.py

StraightBevelGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6188
from mastapy.system_model.analyses_and_results.power_flows import _3320
from mastapy.gears.rating.straight_bevel import _202
from mastapy.system_model.analyses_and_results.system_deflections import _2223
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSystemDeflection',)


class StraightBevelGearSystemDeflection(_2223.BevelGearSystemDeflection):
    '''StraightBevelGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2086.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6188.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6188.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3320.StraightBevelGearPowerFlow':
        '''StraightBevelGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3320.StraightBevelGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_202.StraightBevelGearRating':
        '''StraightBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_202.StraightBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
