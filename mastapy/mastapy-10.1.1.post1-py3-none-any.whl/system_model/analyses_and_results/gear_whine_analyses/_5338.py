'''_5338.py

KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2078
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6144
from mastapy.system_model.analyses_and_results.system_deflections import _2280
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5336, _5337, _5335
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis(_5335.KlingelnbergCycloPalloidConicalGearSetGearWhineAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2078.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2078.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2280.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2280.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5336.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5336.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_gear_whine_analysis(self) -> 'List[_5336.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsGearWhineAnalysis, constructor.new(_5336.KlingelnbergCycloPalloidHypoidGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5337.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5337.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_gear_whine_analysis(self) -> 'List[_5337.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesGearWhineAnalysis, constructor.new(_5337.KlingelnbergCycloPalloidHypoidGearMeshGearWhineAnalysis))
        return value
