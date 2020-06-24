'''_4993.py

KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2350
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4992, _4991, _4987
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses',)


class KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses(_4987.KlingelnbergCycloPalloidConicalGearSetModalAnalysesAtStiffnesses):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses.TYPE'):
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
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_modal_analyses_at_stiffnesses(self) -> 'List[_4992.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsModalAnalysesAtStiffnesses, constructor.new(_4992.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_4991.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesModalAnalysesAtStiffnesses, constructor.new(_4991.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysesAtStiffnesses))
        return value
