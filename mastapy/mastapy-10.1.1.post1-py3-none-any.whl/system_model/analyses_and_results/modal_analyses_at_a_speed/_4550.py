'''_4550.py

SpiralBevelGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2083
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6180
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4549, _4548, _4472
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'SpiralBevelGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetModalAnalysisAtASpeed',)


class SpiralBevelGearSetModalAnalysisAtASpeed(_4472.BevelGearSetModalAnalysisAtASpeed):
    '''SpiralBevelGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2083.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2083.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6180.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6180.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def spiral_bevel_gears_modal_analysis_at_a_speed(self) -> 'List[_4549.SpiralBevelGearModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearModalAnalysisAtASpeed]: 'SpiralBevelGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsModalAnalysisAtASpeed, constructor.new(_4549.SpiralBevelGearModalAnalysisAtASpeed))
        return value

    @property
    def spiral_bevel_meshes_modal_analysis_at_a_speed(self) -> 'List[_4548.SpiralBevelGearMeshModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearMeshModalAnalysisAtASpeed]: 'SpiralBevelMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesModalAnalysisAtASpeed, constructor.new(_4548.SpiralBevelGearMeshModalAnalysisAtASpeed))
        return value
