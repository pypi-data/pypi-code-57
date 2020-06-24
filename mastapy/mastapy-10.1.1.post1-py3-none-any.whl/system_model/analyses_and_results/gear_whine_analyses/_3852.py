'''_3852.py

StraightBevelSunGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2366
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3847
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'StraightBevelSunGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearGearWhineAnalysis',)


class StraightBevelSunGearGearWhineAnalysis(_3847.StraightBevelDiffGearGearWhineAnalysis):
    '''StraightBevelSunGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2366.StraightBevelSunGearSystemDeflection':
        '''StraightBevelSunGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2366.StraightBevelSunGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
