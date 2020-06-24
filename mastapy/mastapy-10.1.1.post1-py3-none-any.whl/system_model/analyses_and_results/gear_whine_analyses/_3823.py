'''_3823.py

BevelDifferentialGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2003
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2315
from mastapy.system_model.analyses_and_results.system_deflections import _2146
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3827
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'BevelDifferentialGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearGearWhineAnalysis',)


class BevelDifferentialGearGearWhineAnalysis(_3827.BevelGearGearWhineAnalysis):
    '''BevelDifferentialGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2003.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2315.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2315.BevelDifferentialGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2146.BevelDifferentialGearSystemDeflection':
        '''BevelDifferentialGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2146.BevelDifferentialGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
