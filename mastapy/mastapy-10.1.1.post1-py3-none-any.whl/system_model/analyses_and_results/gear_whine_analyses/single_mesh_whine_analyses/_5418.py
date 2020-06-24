'''_5418.py

BevelDifferentialGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2055
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6059
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5419, _5417, _5423
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BevelDifferentialGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetSingleMeshWhineAnalysis',)


class BevelDifferentialGearSetSingleMeshWhineAnalysis(_5423.BevelGearSetSingleMeshWhineAnalysis):
    '''BevelDifferentialGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2055.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2055.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6059.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6059.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_single_mesh_whine_analysis(self) -> 'List[_5419.BevelDifferentialGearSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSingleMeshWhineAnalysis]: 'BevelDifferentialGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsSingleMeshWhineAnalysis, constructor.new(_5419.BevelDifferentialGearSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_meshes_single_mesh_whine_analysis(self) -> 'List[_5417.BevelDifferentialGearMeshSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearMeshSingleMeshWhineAnalysis]: 'BevelDifferentialMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesSingleMeshWhineAnalysis, constructor.new(_5417.BevelDifferentialGearMeshSingleMeshWhineAnalysis))
        return value
