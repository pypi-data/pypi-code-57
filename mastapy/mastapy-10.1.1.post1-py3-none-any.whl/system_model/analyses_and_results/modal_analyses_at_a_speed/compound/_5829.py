'''_5829.py

KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _1984
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5827, _5828, _5826
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5710
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed(_5826.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed.TYPE'):
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
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_5827.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysisAtASpeed, constructor.new(_5827.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_5828.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysisAtASpeed, constructor.new(_5828.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5710.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5710.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5710.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_5710.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed))
        return value
