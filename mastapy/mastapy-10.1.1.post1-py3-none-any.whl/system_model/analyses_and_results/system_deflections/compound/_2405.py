'''_2405.py

FlexiblePinAssemblyCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1997
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2266
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2446
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'FlexiblePinAssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyCompoundSystemDeflection',)


class FlexiblePinAssemblyCompoundSystemDeflection(_2446.SpecialisedAssemblyCompoundSystemDeflection):
    '''FlexiblePinAssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1997.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2266.FlexiblePinAssemblySystemDeflection]':
        '''List[FlexiblePinAssemblySystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2266.FlexiblePinAssemblySystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2266.FlexiblePinAssemblySystemDeflection]':
        '''List[FlexiblePinAssemblySystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2266.FlexiblePinAssemblySystemDeflection))
        return value
