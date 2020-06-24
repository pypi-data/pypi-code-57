'''_2551.py

ImportedFEComponentCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1924
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3090
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2540
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ImportedFEComponentCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundAdvancedSystemDeflection',)


class ImportedFEComponentCompoundAdvancedSystemDeflection(_2540.AbstractShaftOrHousingCompoundAdvancedSystemDeflection):
    '''ImportedFEComponentCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3090.ImportedFEComponentAdvancedSystemDeflection]':
        '''List[ImportedFEComponentAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3090.ImportedFEComponentAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_3090.ImportedFEComponentAdvancedSystemDeflection]':
        '''List[ImportedFEComponentAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_3090.ImportedFEComponentAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[ImportedFEComponentCompoundAdvancedSystemDeflection]':
        '''List[ImportedFEComponentCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentCompoundAdvancedSystemDeflection))
        return value
