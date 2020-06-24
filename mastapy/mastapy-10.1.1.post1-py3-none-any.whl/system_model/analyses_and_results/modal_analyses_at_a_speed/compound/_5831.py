'''_5831.py

KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1809
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5711
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5825
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed(_5825.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysisAtASpeed):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5711.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5711.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed))
        return value

    @property
    def connection_modal_analysis_at_a_speed_load_cases(self) -> 'List[_5711.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed]: 'ConnectionModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtASpeedLoadCases, constructor.new(_5711.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtASpeed))
        return value
