'''_2412.py

HypoidGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2074
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2410, _2411, _2359
from mastapy.system_model.analyses_and_results.system_deflections import _2272
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'HypoidGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundSystemDeflection',)


class HypoidGearSetCompoundSystemDeflection(_2359.AGMAGleasonConicalGearSetCompoundSystemDeflection):
    '''HypoidGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2074.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2074.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2074.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2074.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_system_deflection(self) -> 'List[_2410.HypoidGearCompoundSystemDeflection]':
        '''List[HypoidGearCompoundSystemDeflection]: 'HypoidGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundSystemDeflection, constructor.new(_2410.HypoidGearCompoundSystemDeflection))
        return value

    @property
    def hypoid_meshes_compound_system_deflection(self) -> 'List[_2411.HypoidGearMeshCompoundSystemDeflection]':
        '''List[HypoidGearMeshCompoundSystemDeflection]: 'HypoidMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundSystemDeflection, constructor.new(_2411.HypoidGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2272.HypoidGearSetSystemDeflection]':
        '''List[HypoidGearSetSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2272.HypoidGearSetSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2272.HypoidGearSetSystemDeflection]':
        '''List[HypoidGearSetSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2272.HypoidGearSetSystemDeflection))
        return value
