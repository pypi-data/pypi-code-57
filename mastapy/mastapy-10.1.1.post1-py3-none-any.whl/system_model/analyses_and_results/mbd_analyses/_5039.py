'''_5039.py

KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2078
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6144
from mastapy.system_model.analyses_and_results.mbd_analyses import _5038, _5037, _5036
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis(_5036.KlingelnbergCycloPalloidConicalGearSetMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2078.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2078.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5038.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5038.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_multi_body_dynamics_analysis(self) -> 'List[_5038.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsMultiBodyDynamicsAnalysis, constructor.new(_5038.KlingelnbergCycloPalloidHypoidGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_multi_body_dynamics_analysis(self) -> 'List[_5037.KlingelnbergCycloPalloidHypoidGearMeshMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesMultiBodyDynamicsAnalysis, constructor.new(_5037.KlingelnbergCycloPalloidHypoidGearMeshMultiBodyDynamicsAnalysis))
        return value
