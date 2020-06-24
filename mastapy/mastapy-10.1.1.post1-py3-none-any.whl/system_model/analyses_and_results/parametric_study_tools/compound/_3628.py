'''_3628.py

ConceptGearMeshCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1866
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3490
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3652
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConceptGearMeshCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundParametricStudyTool',)


class ConceptGearMeshCompoundParametricStudyTool(_3652.GearMeshCompoundParametricStudyTool):
    '''ConceptGearMeshCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1866.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1866.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1866.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1866.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3490.ConceptGearMeshParametricStudyTool]':
        '''List[ConceptGearMeshParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3490.ConceptGearMeshParametricStudyTool))
        return value

    @property
    def connection_parametric_study_tool_load_cases(self) -> 'List[_3490.ConceptGearMeshParametricStudyTool]':
        '''List[ConceptGearMeshParametricStudyTool]: 'ConnectionParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionParametricStudyToolLoadCases, constructor.new(_3490.ConceptGearMeshParametricStudyTool))
        return value
