'''_5266.py

BevelDifferentialSunGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2057
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2220
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5262
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'BevelDifferentialSunGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearGearWhineAnalysis',)


class BevelDifferentialSunGearGearWhineAnalysis(_5262.BevelDifferentialGearGearWhineAnalysis):
    '''BevelDifferentialSunGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2057.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2057.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2220.BevelDifferentialSunGearSystemDeflection':
        '''BevelDifferentialSunGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2220.BevelDifferentialSunGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
