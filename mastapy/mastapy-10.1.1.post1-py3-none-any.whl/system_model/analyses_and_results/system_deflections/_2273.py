'''_2273.py

HypoidGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2073
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6133
from mastapy.system_model.analyses_and_results.power_flows import _3273
from mastapy.gears.rating.hypoid import _241
from mastapy.system_model.analyses_and_results.system_deflections import _2211
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'HypoidGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSystemDeflection',)


class HypoidGearSystemDeflection(_2211.AGMAGleasonConicalGearSystemDeflection):
    '''HypoidGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSystemDeflection.TYPE'):
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

    @property
    def power_flow_results(self) -> '_3273.HypoidGearPowerFlow':
        '''HypoidGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3273.HypoidGearPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_241.HypoidGearRating':
        '''HypoidGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_241.HypoidGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
