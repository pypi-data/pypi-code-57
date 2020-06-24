'''_5111.py

KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1808
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4988
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5108
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtStiffnesses',)


class KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtStiffnesses(_5108.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysesAtStiffnesses):
    '''KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4988.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4988.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtStiffnesses))
        return value

    @property
    def connection_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_4988.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtStiffnesses]: 'ConnectionModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtStiffnessesLoadCases, constructor.new(_4988.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysesAtStiffnesses))
        return value
