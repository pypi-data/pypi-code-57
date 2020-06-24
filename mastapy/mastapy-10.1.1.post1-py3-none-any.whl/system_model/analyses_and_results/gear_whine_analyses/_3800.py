'''_3800.py

FlexiblePinAssemblyGearWhineAnalysis
'''


from mastapy.system_model.part_model import _1920
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2276
from mastapy.system_model.analyses_and_results.system_deflections import _2275
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3813
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'FlexiblePinAssemblyGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyGearWhineAnalysis',)


class FlexiblePinAssemblyGearWhineAnalysis(_3813.SpecialisedAssemblyGearWhineAnalysis):
    '''FlexiblePinAssemblyGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1920.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1920.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2276.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2276.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2275.FlexiblePinAssemblySystemDeflection':
        '''FlexiblePinAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.FlexiblePinAssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
