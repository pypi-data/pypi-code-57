'''_4208.py

WormGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2091
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4206, _4207, _4144
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4087
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'WormGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundModalAnalysesAtSpeeds',)


class WormGearSetCompoundModalAnalysesAtSpeeds(_4144.GearSetCompoundModalAnalysesAtSpeeds):
    '''WormGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2091.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2091.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2091.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2091.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_modal_analyses_at_speeds(self) -> 'List[_4206.WormGearCompoundModalAnalysesAtSpeeds]':
        '''List[WormGearCompoundModalAnalysesAtSpeeds]: 'WormGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundModalAnalysesAtSpeeds, constructor.new(_4206.WormGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def worm_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_4207.WormGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[WormGearMeshCompoundModalAnalysesAtSpeeds]: 'WormMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_4207.WormGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4087.WormGearSetModalAnalysesAtSpeeds]':
        '''List[WormGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4087.WormGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_4087.WormGearSetModalAnalysesAtSpeeds]':
        '''List[WormGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_4087.WormGearSetModalAnalysesAtSpeeds))
        return value
