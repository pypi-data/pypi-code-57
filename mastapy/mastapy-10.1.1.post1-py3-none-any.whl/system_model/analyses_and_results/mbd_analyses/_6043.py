'''_6043.py

ZerolBevelGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2236
from mastapy.system_model.analyses_and_results.mbd_analyses import _6042, _6041, _5926
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ZerolBevelGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetMultiBodyDynamicsAnalysis',)


class ZerolBevelGearSetMultiBodyDynamicsAnalysis(_5926.BevelGearSetMultiBodyDynamicsAnalysis):
    '''ZerolBevelGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2013.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2236.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_6042.ZerolBevelGearMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6042.ZerolBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gears_multi_body_dynamics_analysis(self) -> 'List[_6042.ZerolBevelGearMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultiBodyDynamicsAnalysis]: 'ZerolBevelGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsMultiBodyDynamicsAnalysis, constructor.new(_6042.ZerolBevelGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_meshes_multi_body_dynamics_analysis(self) -> 'List[_6041.ZerolBevelGearMeshMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMeshMultiBodyDynamicsAnalysis]: 'ZerolBevelMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesMultiBodyDynamicsAnalysis, constructor.new(_6041.ZerolBevelGearMeshMultiBodyDynamicsAnalysis))
        return value
