'''_4316.py

StraightBevelGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2087
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6190
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4315, _4314, _4228
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'StraightBevelGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetModalAnalysisAtAStiffness',)


class StraightBevelGearSetModalAnalysisAtAStiffness(_4228.BevelGearSetModalAnalysisAtAStiffness):
    '''StraightBevelGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2087.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6190.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6190.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4315.StraightBevelGearModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearModalAnalysisAtAStiffness]: 'StraightBevelGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsModalAnalysisAtAStiffness, constructor.new(_4315.StraightBevelGearModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4314.StraightBevelGearMeshModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearMeshModalAnalysisAtAStiffness]: 'StraightBevelMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesModalAnalysisAtAStiffness, constructor.new(_4314.StraightBevelGearMeshModalAnalysisAtAStiffness))
        return value
