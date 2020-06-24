'''_2618.py

SynchroniserCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1976
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2197
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2603
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SynchroniserCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundSystemDeflection',)


class SynchroniserCompoundSystemDeflection(_2603.SpecialisedAssemblyCompoundSystemDeflection):
    '''SynchroniserCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1976.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1976.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2197.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2197.SynchroniserSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2197.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2197.SynchroniserSystemDeflection))
        return value
