'''_3398.py

SpringDamperAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1990
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2194
from mastapy.system_model.analyses_and_results.system_deflections import _2193
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3390
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'SpringDamperAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperAdvancedSystemDeflection',)


class SpringDamperAdvancedSystemDeflection(_3390.CouplingAdvancedSystemDeflection):
    '''SpringDamperAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1990.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2194.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2193.SpringDamperSystemDeflection]':
        '''List[SpringDamperSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2193.SpringDamperSystemDeflection))
        return value
