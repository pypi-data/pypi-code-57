'''_4016.py

StraightBevelDiffGearMeshParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1814
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2238
from mastapy.system_model.analyses_and_results.system_deflections import _2237
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4017
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'StraightBevelDiffGearMeshParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshParametricStudyTool',)


class StraightBevelDiffGearMeshParametricStudyTool(_4017.BevelGearMeshParametricStudyTool):
    '''StraightBevelDiffGearMeshParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2238.StraightBevelDiffGearMeshLoadCase':
        '''StraightBevelDiffGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2238.StraightBevelDiffGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2237.StraightBevelDiffGearMeshSystemDeflection]':
        '''List[StraightBevelDiffGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection))
        return value
