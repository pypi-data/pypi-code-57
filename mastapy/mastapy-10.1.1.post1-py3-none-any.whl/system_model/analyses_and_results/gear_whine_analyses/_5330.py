'''_5330.py

HypoidGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2074
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6135
from mastapy.system_model.analyses_and_results.system_deflections import _2272
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5328, _5329, _5257
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'HypoidGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetGearWhineAnalysis',)


class HypoidGearSetGearWhineAnalysis(_5257.AGMAGleasonConicalGearSetGearWhineAnalysis):
    '''HypoidGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2074.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2074.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6135.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6135.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2272.HypoidGearSetSystemDeflection':
        '''HypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2272.HypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5328.HypoidGearGearWhineAnalysis]':
        '''List[HypoidGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5328.HypoidGearGearWhineAnalysis))
        return value

    @property
    def hypoid_gears_gear_whine_analysis(self) -> 'List[_5328.HypoidGearGearWhineAnalysis]':
        '''List[HypoidGearGearWhineAnalysis]: 'HypoidGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsGearWhineAnalysis, constructor.new(_5328.HypoidGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5329.HypoidGearMeshGearWhineAnalysis]':
        '''List[HypoidGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5329.HypoidGearMeshGearWhineAnalysis))
        return value

    @property
    def hypoid_meshes_gear_whine_analysis(self) -> 'List[_5329.HypoidGearMeshGearWhineAnalysis]':
        '''List[HypoidGearMeshGearWhineAnalysis]: 'HypoidMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesGearWhineAnalysis, constructor.new(_5329.HypoidGearMeshGearWhineAnalysis))
        return value
