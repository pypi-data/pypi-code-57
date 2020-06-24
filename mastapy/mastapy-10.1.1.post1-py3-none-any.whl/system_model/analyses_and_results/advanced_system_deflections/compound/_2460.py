'''_2460.py

KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2012
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3486
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2458
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection(_2458.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2012.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection))
        return value
