'''_3106.py

FaceGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1987
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2338
from mastapy.gears.rating.face import _470
from mastapy.system_model.analyses_and_results.system_deflections import _2194
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3121
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FaceGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearAdvancedSystemDeflection',)


class FaceGearAdvancedSystemDeflection(_3121.GearAdvancedSystemDeflection):
    '''FaceGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1987.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2338.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2338.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_470.FaceGearRating':
        '''FaceGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_470.FaceGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_system_deflection_results(self) -> 'List[_2194.FaceGearSystemDeflection]':
        '''List[FaceGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2194.FaceGearSystemDeflection))
        return value
