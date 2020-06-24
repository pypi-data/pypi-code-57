'''_5372.py

SpringDamperHalfGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2134
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6182
from mastapy.system_model.analyses_and_results.system_deflections import _2315
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5291
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SpringDamperHalfGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfGearWhineAnalysis',)


class SpringDamperHalfGearWhineAnalysis(_5291.CouplingHalfGearWhineAnalysis):
    '''SpringDamperHalfGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2134.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6182.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6182.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2315.SpringDamperHalfSystemDeflection':
        '''SpringDamperHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.SpringDamperHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
