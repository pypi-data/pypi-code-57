'''_2663.py

ConceptGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2661, _2662, _2687
from mastapy.system_model.analyses_and_results.system_deflections import _2164
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConceptGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundSystemDeflection',)


class ConceptGearSetCompoundSystemDeflection(_2687.GearSetCompoundSystemDeflection):
    '''ConceptGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1978.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1978.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_system_deflection(self) -> 'List[_2661.ConceptGearCompoundSystemDeflection]':
        '''List[ConceptGearCompoundSystemDeflection]: 'ConceptGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundSystemDeflection, constructor.new(_2661.ConceptGearCompoundSystemDeflection))
        return value

    @property
    def concept_meshes_compound_system_deflection(self) -> 'List[_2662.ConceptGearMeshCompoundSystemDeflection]':
        '''List[ConceptGearMeshCompoundSystemDeflection]: 'ConceptMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundSystemDeflection, constructor.new(_2662.ConceptGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2164.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2164.ConceptGearSetSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2164.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2164.ConceptGearSetSystemDeflection))
        return value
