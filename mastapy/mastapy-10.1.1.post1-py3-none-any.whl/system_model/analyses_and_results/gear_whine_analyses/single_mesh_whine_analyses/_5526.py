'''_5526.py

WormGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2091
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6211
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5527, _5525, _5460
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'WormGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetSingleMeshWhineAnalysis',)


class WormGearSetSingleMeshWhineAnalysis(_5460.GearSetSingleMeshWhineAnalysis):
    '''WormGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2091.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2091.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6211.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6211.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_single_mesh_whine_analysis(self) -> 'List[_5527.WormGearSingleMeshWhineAnalysis]':
        '''List[WormGearSingleMeshWhineAnalysis]: 'WormGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsSingleMeshWhineAnalysis, constructor.new(_5527.WormGearSingleMeshWhineAnalysis))
        return value

    @property
    def worm_meshes_single_mesh_whine_analysis(self) -> 'List[_5525.WormGearMeshSingleMeshWhineAnalysis]':
        '''List[WormGearMeshSingleMeshWhineAnalysis]: 'WormMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesSingleMeshWhineAnalysis, constructor.new(_5525.WormGearMeshSingleMeshWhineAnalysis))
        return value
