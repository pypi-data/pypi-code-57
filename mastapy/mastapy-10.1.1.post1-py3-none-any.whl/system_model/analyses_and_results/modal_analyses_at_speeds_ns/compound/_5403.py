'''_5403.py

ZerolBevelGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5405, _5406, _5305
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5288
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ZerolBevelGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundModalAnalysesAtSpeeds',)


class ZerolBevelGearSetCompoundModalAnalysesAtSpeeds(_5305.BevelGearSetCompoundModalAnalysesAtSpeeds):
    '''ZerolBevelGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_modal_analyses_at_speeds(self) -> 'List[_5405.ZerolBevelGearCompoundModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearCompoundModalAnalysesAtSpeeds]: 'ZerolBevelGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundModalAnalysesAtSpeeds, constructor.new(_5405.ZerolBevelGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_5406.ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds]: 'ZerolBevelMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_5406.ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5288.ZerolBevelGearSetModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5288.ZerolBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_5288.ZerolBevelGearSetModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_5288.ZerolBevelGearSetModalAnalysesAtSpeeds))
        return value
