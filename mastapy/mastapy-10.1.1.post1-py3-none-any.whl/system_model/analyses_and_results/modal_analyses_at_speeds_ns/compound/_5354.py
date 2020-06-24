'''_5354.py

KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5352, _5353, _5351
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5233
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds(_5351.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysesAtSpeeds):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_modal_analyses_at_speeds(self) -> 'List[_5352.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysesAtSpeeds, constructor.new(_5352.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_5353.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_5353.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5233.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5233.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_5233.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_5233.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds))
        return value
