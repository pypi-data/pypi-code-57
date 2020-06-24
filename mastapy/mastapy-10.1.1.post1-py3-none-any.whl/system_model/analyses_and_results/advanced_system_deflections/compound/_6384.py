'''_6384.py

ConceptCouplingCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6259
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6395
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ConceptCouplingCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingCompoundAdvancedSystemDeflection',)


class ConceptCouplingCompoundAdvancedSystemDeflection(_6395.CouplingCompoundAdvancedSystemDeflection):
    '''ConceptCouplingCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2116.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6259.ConceptCouplingAdvancedSystemDeflection]':
        '''List[ConceptCouplingAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6259.ConceptCouplingAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_6259.ConceptCouplingAdvancedSystemDeflection]':
        '''List[ConceptCouplingAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_6259.ConceptCouplingAdvancedSystemDeflection))
        return value
