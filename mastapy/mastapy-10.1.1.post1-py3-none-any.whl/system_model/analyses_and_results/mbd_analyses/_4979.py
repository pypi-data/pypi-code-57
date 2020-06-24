'''_4979.py

BevelDifferentialGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2055
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6059
from mastapy.system_model.analyses_and_results.mbd_analyses import _4978, _4977, _4984
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BevelDifferentialGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetMultiBodyDynamicsAnalysis',)


class BevelDifferentialGearSetMultiBodyDynamicsAnalysis(_4984.BevelGearSetMultiBodyDynamicsAnalysis):
    '''BevelDifferentialGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetMultiBodyDynamicsAnalysis.TYPE'):
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
    def gears(self) -> 'List[_4978.BevelDifferentialGearMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_4978.BevelDifferentialGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gears_multi_body_dynamics_analysis(self) -> 'List[_4978.BevelDifferentialGearMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMultiBodyDynamicsAnalysis]: 'BevelDifferentialGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsMultiBodyDynamicsAnalysis, constructor.new(_4978.BevelDifferentialGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_meshes_multi_body_dynamics_analysis(self) -> 'List[_4977.BevelDifferentialGearMeshMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearMeshMultiBodyDynamicsAnalysis]: 'BevelDifferentialMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesMultiBodyDynamicsAnalysis, constructor.new(_4977.BevelDifferentialGearMeshMultiBodyDynamicsAnalysis))
        return value
