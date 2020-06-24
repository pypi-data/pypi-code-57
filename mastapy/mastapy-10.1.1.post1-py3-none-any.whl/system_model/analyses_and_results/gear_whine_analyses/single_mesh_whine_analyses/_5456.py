'''_5456.py

FaceGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6115
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5457, _5455, _5460
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'FaceGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetSingleMeshWhineAnalysis',)


class FaceGearSetSingleMeshWhineAnalysis(_5460.GearSetSingleMeshWhineAnalysis):
    '''FaceGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6115.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6115.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_single_mesh_whine_analysis(self) -> 'List[_5457.FaceGearSingleMeshWhineAnalysis]':
        '''List[FaceGearSingleMeshWhineAnalysis]: 'FaceGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsSingleMeshWhineAnalysis, constructor.new(_5457.FaceGearSingleMeshWhineAnalysis))
        return value

    @property
    def face_meshes_single_mesh_whine_analysis(self) -> 'List[_5455.FaceGearMeshSingleMeshWhineAnalysis]':
        '''List[FaceGearMeshSingleMeshWhineAnalysis]: 'FaceMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesSingleMeshWhineAnalysis, constructor.new(_5455.FaceGearMeshSingleMeshWhineAnalysis))
        return value
