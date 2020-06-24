'''_2450.py

SpringDamperCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2133
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2316
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2390
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SpringDamperCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundSystemDeflection',)


class SpringDamperCompoundSystemDeflection(_2390.CouplingCompoundSystemDeflection):
    '''SpringDamperCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2133.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2133.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2316.SpringDamperSystemDeflection]':
        '''List[SpringDamperSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2316.SpringDamperSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2316.SpringDamperSystemDeflection]':
        '''List[SpringDamperSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2316.SpringDamperSystemDeflection))
        return value
