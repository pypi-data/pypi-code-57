'''_3040.py

SpringDamperHalfAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2043
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2254
from mastapy.system_model.analyses_and_results.system_deflections import _2253
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3032
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'SpringDamperHalfAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfAdvancedSystemDeflection',)


class SpringDamperHalfAdvancedSystemDeflection(_3032.CouplingHalfAdvancedSystemDeflection):
    '''SpringDamperHalfAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2043.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2043.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2254.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2254.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2253.SpringDamperHalfSystemDeflection]':
        '''List[SpringDamperHalfSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2253.SpringDamperHalfSystemDeflection))
        return value
