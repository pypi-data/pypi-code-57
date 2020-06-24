'''_5821.py

HypoidGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _1965
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5819, _5820, _5768
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5702
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'HypoidGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundModalAnalysisAtASpeed',)


class HypoidGearSetCompoundModalAnalysisAtASpeed(_5768.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed):
    '''HypoidGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_5819.HypoidGearCompoundModalAnalysisAtASpeed]':
        '''List[HypoidGearCompoundModalAnalysisAtASpeed]: 'HypoidGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundModalAnalysisAtASpeed, constructor.new(_5819.HypoidGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def hypoid_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_5820.HypoidGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[HypoidGearMeshCompoundModalAnalysisAtASpeed]: 'HypoidMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundModalAnalysisAtASpeed, constructor.new(_5820.HypoidGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5702.HypoidGearSetModalAnalysisAtASpeed]':
        '''List[HypoidGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5702.HypoidGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5702.HypoidGearSetModalAnalysisAtASpeed]':
        '''List[HypoidGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_5702.HypoidGearSetModalAnalysisAtASpeed))
        return value
