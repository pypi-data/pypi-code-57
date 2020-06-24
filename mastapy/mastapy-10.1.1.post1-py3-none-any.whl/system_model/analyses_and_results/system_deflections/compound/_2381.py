'''_2381.py

ConceptCouplingHalfCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2117
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2233
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2392
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConceptCouplingHalfCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfCompoundSystemDeflection',)


class ConceptCouplingHalfCompoundSystemDeflection(_2392.CouplingHalfCompoundSystemDeflection):
    '''ConceptCouplingHalfCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2117.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2233.ConceptCouplingHalfSystemDeflection]':
        '''List[ConceptCouplingHalfSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2233.ConceptCouplingHalfSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2233.ConceptCouplingHalfSystemDeflection]':
        '''List[ConceptCouplingHalfSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2233.ConceptCouplingHalfSystemDeflection))
        return value
