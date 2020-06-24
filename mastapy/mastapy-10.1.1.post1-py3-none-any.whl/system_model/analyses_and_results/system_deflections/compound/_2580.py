'''_2580.py

KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2578, _2579, _2577
from mastapy.system_model.analyses_and_results.system_deflections import _2345
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection(_2577.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_system_deflection(self) -> 'List[_2578.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundSystemDeflection, constructor.new(_2578.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_system_deflection(self) -> 'List[_2579.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundSystemDeflection, constructor.new(_2579.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value
