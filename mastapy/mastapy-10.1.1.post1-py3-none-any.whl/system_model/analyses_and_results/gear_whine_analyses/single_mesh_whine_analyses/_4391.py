'''_4391.py

StraightBevelDiffGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1982
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2359
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4390, _4320, _4371
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'StraightBevelDiffGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetSingleMeshWhineAnalysis',)


class StraightBevelDiffGearSetSingleMeshWhineAnalysis(_4371.BevelGearSetSingleMeshWhineAnalysis):
    '''StraightBevelDiffGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1982.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2359.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2359.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_single_mesh_whine_analysis(self) -> 'List[_4390.StraightBevelDiffGearSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSingleMeshWhineAnalysis]: 'StraightBevelDiffGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsSingleMeshWhineAnalysis, constructor.new(_4390.StraightBevelDiffGearSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_single_mesh_whine_analysis(self) -> 'List[_4320.StraightBevelDiffGearMeshSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshSingleMeshWhineAnalysis]: 'StraightBevelDiffMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesSingleMeshWhineAnalysis, constructor.new(_4320.StraightBevelDiffGearMeshSingleMeshWhineAnalysis))
        return value
