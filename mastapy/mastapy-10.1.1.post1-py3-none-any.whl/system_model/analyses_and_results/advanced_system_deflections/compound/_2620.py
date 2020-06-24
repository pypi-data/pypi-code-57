'''_2620.py

SynchroniserCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2032
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3041
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2561
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'SynchroniserCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundAdvancedSystemDeflection',)


class SynchroniserCompoundAdvancedSystemDeflection(_2561.SpecialisedAssemblyCompoundAdvancedSystemDeflection):
    '''SynchroniserCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2032.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2032.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2032.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3041.SynchroniserAdvancedSystemDeflection]':
        '''List[SynchroniserAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3041.SynchroniserAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_3041.SynchroniserAdvancedSystemDeflection]':
        '''List[SynchroniserAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_3041.SynchroniserAdvancedSystemDeflection))
        return value
