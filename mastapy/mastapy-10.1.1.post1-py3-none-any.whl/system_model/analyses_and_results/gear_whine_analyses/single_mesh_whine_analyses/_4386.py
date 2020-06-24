'''_4386.py

KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2350
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4385, _4328, _4382
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis(_4382.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_single_mesh_whine_analysis(self) -> 'List[_4385.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsSingleMeshWhineAnalysis, constructor.new(_4385.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_single_mesh_whine_analysis(self) -> 'List[_4328.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesSingleMeshWhineAnalysis, constructor.new(_4328.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis))
        return value
