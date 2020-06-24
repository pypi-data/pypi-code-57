'''_3735.py

ZerolBevelGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2012
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2234
from mastapy.system_model.analyses_and_results.system_deflections import _2233
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3825
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ZerolBevelGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearGearWhineAnalysis',)


class ZerolBevelGearGearWhineAnalysis(_3825.BevelGearGearWhineAnalysis):
    '''ZerolBevelGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2234.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2234.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2233.ZerolBevelGearSystemDeflection':
        '''ZerolBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2233.ZerolBevelGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
