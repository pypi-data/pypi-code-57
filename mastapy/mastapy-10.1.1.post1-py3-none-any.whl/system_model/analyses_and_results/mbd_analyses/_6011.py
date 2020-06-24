'''_6011.py

SpiralBevelGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1966
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2355
from mastapy.system_model.analyses_and_results.mbd_analyses import _6010, _6009, _5925
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpiralBevelGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetMultiBodyDynamicsAnalysis',)


class SpiralBevelGearSetMultiBodyDynamicsAnalysis(_5925.BevelGearSetMultiBodyDynamicsAnalysis):
    '''SpiralBevelGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2355.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2355.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_6010.SpiralBevelGearMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6010.SpiralBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gears_multi_body_dynamics_analysis(self) -> 'List[_6010.SpiralBevelGearMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMultiBodyDynamicsAnalysis]: 'SpiralBevelGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsMultiBodyDynamicsAnalysis, constructor.new(_6010.SpiralBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_meshes_multi_body_dynamics_analysis(self) -> 'List[_6009.SpiralBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMeshMultiBodyDynamicsAnalysis]: 'SpiralBevelMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesMultiBodyDynamicsAnalysis, constructor.new(_6009.SpiralBevelGearMeshMultiBodyDynamicsAnalysis))
        return value
