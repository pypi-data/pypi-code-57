'''_4090.py

ZerolBevelGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2093
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6214
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4089, _4088, _3982
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ZerolBevelGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetModalAnalysesAtSpeeds',)


class ZerolBevelGearSetModalAnalysesAtSpeeds(_3982.BevelGearSetModalAnalysesAtSpeeds):
    '''ZerolBevelGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2093.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2093.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6214.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6214.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_modal_analyses_at_speeds(self) -> 'List[_4089.ZerolBevelGearModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearModalAnalysesAtSpeeds]: 'ZerolBevelGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsModalAnalysesAtSpeeds, constructor.new(_4089.ZerolBevelGearModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_meshes_modal_analyses_at_speeds(self) -> 'List[_4088.ZerolBevelGearMeshModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearMeshModalAnalysesAtSpeeds]: 'ZerolBevelMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesModalAnalysesAtSpeeds, constructor.new(_4088.ZerolBevelGearMeshModalAnalysesAtSpeeds))
        return value
