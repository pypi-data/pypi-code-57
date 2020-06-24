'''_2718.py

ShaftCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _1942
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2719, _2398
from mastapy.system_model.analyses_and_results.system_deflections import _2065
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ShaftCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundSystemDeflection',)


class ShaftCompoundSystemDeflection(_2398.AbstractShaftOrHousingCompoundSystemDeflection):
    '''ShaftCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def shaft_duty_cycle_damage_results(self) -> '_2719.ShaftDutyCycleSystemDeflection':
        '''ShaftDutyCycleSystemDeflection: 'ShaftDutyCycleDamageResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2719.ShaftDutyCycleSystemDeflection)(self.wrapped.ShaftDutyCycleDamageResults) if self.wrapped.ShaftDutyCycleDamageResults else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2065.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2065.ShaftSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2065.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2065.ShaftSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundSystemDeflection]':
        '''List[ShaftCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundSystemDeflection))
        return value
