'''_3701.py

StraightBevelGearMeshCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1888
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3579
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3615
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'StraightBevelGearMeshCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMeshCompoundParametricStudyTool',)


class StraightBevelGearMeshCompoundParametricStudyTool(_3615.BevelGearMeshCompoundParametricStudyTool):
    '''StraightBevelGearMeshCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMeshCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1888.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1888.StraightBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1888.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1888.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3579.StraightBevelGearMeshParametricStudyTool]':
        '''List[StraightBevelGearMeshParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3579.StraightBevelGearMeshParametricStudyTool))
        return value

    @property
    def connection_parametric_study_tool_load_cases(self) -> 'List[_3579.StraightBevelGearMeshParametricStudyTool]':
        '''List[StraightBevelGearMeshParametricStudyTool]: 'ConnectionParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionParametricStudyToolLoadCases, constructor.new(_3579.StraightBevelGearMeshParametricStudyTool))
        return value
