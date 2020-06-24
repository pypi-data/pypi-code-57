'''_4159.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2080
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4157, _4158, _4153
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4035
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds(_4153.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysesAtSpeeds):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2080.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2080.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_modal_analyses_at_speeds(self) -> 'List[_4157.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysesAtSpeeds, constructor.new(_4157.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_4158.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_4158.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4035.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4035.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_4035.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_4035.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds))
        return value
