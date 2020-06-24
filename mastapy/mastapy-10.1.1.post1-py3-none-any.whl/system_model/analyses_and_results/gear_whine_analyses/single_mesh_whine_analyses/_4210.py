'''_4210.py

ZerolBevelGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1991
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2171
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4209, _4261, _4300
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ZerolBevelGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetSingleMeshWhineAnalysis',)


class ZerolBevelGearSetSingleMeshWhineAnalysis(_4300.BevelGearSetSingleMeshWhineAnalysis):
    '''ZerolBevelGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1991.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2171.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2171.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_single_mesh_whine_analysis(self) -> 'List[_4209.ZerolBevelGearSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSingleMeshWhineAnalysis]: 'ZerolBevelGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsSingleMeshWhineAnalysis, constructor.new(_4209.ZerolBevelGearSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_meshes_single_mesh_whine_analysis(self) -> 'List[_4261.ZerolBevelGearMeshSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearMeshSingleMeshWhineAnalysis]: 'ZerolBevelMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesSingleMeshWhineAnalysis, constructor.new(_4261.ZerolBevelGearMeshSingleMeshWhineAnalysis))
        return value
