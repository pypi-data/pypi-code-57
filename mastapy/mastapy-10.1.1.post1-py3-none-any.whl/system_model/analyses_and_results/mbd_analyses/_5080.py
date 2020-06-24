'''_5080.py

StraightBevelDiffGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2085
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6187
from mastapy.system_model.analyses_and_results.mbd_analyses import _5079, _5078, _4984
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelDiffGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetMultiBodyDynamicsAnalysis',)


class StraightBevelDiffGearSetMultiBodyDynamicsAnalysis(_4984.BevelGearSetMultiBodyDynamicsAnalysis):
    '''StraightBevelDiffGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2085.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2085.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6187.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6187.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5079.StraightBevelDiffGearMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5079.StraightBevelDiffGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gears_multi_body_dynamics_analysis(self) -> 'List[_5079.StraightBevelDiffGearMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMultiBodyDynamicsAnalysis]: 'StraightBevelDiffGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsMultiBodyDynamicsAnalysis, constructor.new(_5079.StraightBevelDiffGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_multi_body_dynamics_analysis(self) -> 'List[_5078.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]: 'StraightBevelDiffMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesMultiBodyDynamicsAnalysis, constructor.new(_5078.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis))
        return value
