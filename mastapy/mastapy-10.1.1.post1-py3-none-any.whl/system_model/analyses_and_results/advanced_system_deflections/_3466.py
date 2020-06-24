'''_3466.py

FaceGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2312
from mastapy.gears.rating.face import _396
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3465, _3422, _3481
from mastapy.system_model.analyses_and_results.system_deflections import _2311
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FaceGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetAdvancedSystemDeflection',)


class FaceGearSetAdvancedSystemDeflection(_3481.GearSetAdvancedSystemDeflection):
    '''FaceGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2312.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2312.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_396.FaceGearSetRating':
        '''FaceGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_396.FaceGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_396.FaceGearSetRating':
        '''FaceGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_396.FaceGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def face_gears_advanced_system_deflection(self) -> 'List[_3465.FaceGearAdvancedSystemDeflection]':
        '''List[FaceGearAdvancedSystemDeflection]: 'FaceGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsAdvancedSystemDeflection, constructor.new(_3465.FaceGearAdvancedSystemDeflection))
        return value

    @property
    def face_meshes_advanced_system_deflection(self) -> 'List[_3422.FaceGearMeshAdvancedSystemDeflection]':
        '''List[FaceGearMeshAdvancedSystemDeflection]: 'FaceMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesAdvancedSystemDeflection, constructor.new(_3422.FaceGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2311.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2311.FaceGearSetSystemDeflection))
        return value
