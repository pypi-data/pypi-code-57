'''_2202.py

HypoidGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _1993
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2355
from mastapy.gears.rating.hypoid import _463
from mastapy.system_model.analyses_and_results.system_deflections import _2140
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'HypoidGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSystemDeflection',)


class HypoidGearSystemDeflection(_2140.AGMAGleasonConicalGearSystemDeflection):
    '''HypoidGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1993.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2355.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2355.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_463.HypoidGearRating':
        '''HypoidGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_463.HypoidGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
