'''_3752.py

SpringDamperGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _1990
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2194
from mastapy.system_model.analyses_and_results.system_deflections import _2193
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3744
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SpringDamperGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperGearWhineAnalysis',)


class SpringDamperGearWhineAnalysis(_3744.CouplingGearWhineAnalysis):
    '''SpringDamperGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1990.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2194.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2193.SpringDamperSystemDeflection':
        '''SpringDamperSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.SpringDamperSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
