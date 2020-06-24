'''_3223.py

ConceptGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3222, _3180, _3240
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4054
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConceptGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundParametricStudyTool',)


class ConceptGearSetCompoundParametricStudyTool(_3240.GearSetCompoundParametricStudyTool):
    '''ConceptGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1981.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1981.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_parametric_study_tool(self) -> 'List[_3222.ConceptGearCompoundParametricStudyTool]':
        '''List[ConceptGearCompoundParametricStudyTool]: 'ConceptGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundParametricStudyTool, constructor.new(_3222.ConceptGearCompoundParametricStudyTool))
        return value

    @property
    def concept_meshes_compound_parametric_study_tool(self) -> 'List[_3180.ConceptGearMeshCompoundParametricStudyTool]':
        '''List[ConceptGearMeshCompoundParametricStudyTool]: 'ConceptMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundParametricStudyTool, constructor.new(_3180.ConceptGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4054.ConceptGearSetParametricStudyTool]':
        '''List[ConceptGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4054.ConceptGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4054.ConceptGearSetParametricStudyTool]':
        '''List[ConceptGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4054.ConceptGearSetParametricStudyTool))
        return value
