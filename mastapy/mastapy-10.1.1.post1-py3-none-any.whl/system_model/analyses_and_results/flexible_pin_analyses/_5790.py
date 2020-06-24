'''_5790.py

FlexiblePinAnalysisGearAndBearingRating
'''


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections.compound import _2398, _2361
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5787
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_GEAR_AND_BEARING_RATING = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisGearAndBearingRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisGearAndBearingRating',)


class FlexiblePinAnalysisGearAndBearingRating(_5787.FlexiblePinAnalysis):
    '''FlexiblePinAnalysisGearAndBearingRating

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ANALYSIS_GEAR_AND_BEARING_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisGearAndBearingRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_set_analysis(self) -> '_2398.CylindricalGearSetCompoundSystemDeflection':
        '''CylindricalGearSetCompoundSystemDeflection: 'GearSetAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2398.CylindricalGearSetCompoundSystemDeflection)(self.wrapped.GearSetAnalysis) if self.wrapped.GearSetAnalysis else None

    @property
    def bearing_analyses(self) -> 'List[_2361.BearingCompoundSystemDeflection]':
        '''List[BearingCompoundSystemDeflection]: 'BearingAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingAnalyses, constructor.new(_2361.BearingCompoundSystemDeflection))
        return value
