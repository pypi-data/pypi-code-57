'''_3961.py

WormGearMeshCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1890
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3839
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3897
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'WormGearMeshCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundModalAnalysesAtStiffnesses',)


class WormGearMeshCompoundModalAnalysesAtStiffnesses(_3897.GearMeshCompoundModalAnalysesAtStiffnesses):
    '''WormGearMeshCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1890.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1890.WormGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1890.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1890.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3839.WormGearMeshModalAnalysesAtStiffnesses]':
        '''List[WormGearMeshModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3839.WormGearMeshModalAnalysesAtStiffnesses))
        return value

    @property
    def connection_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3839.WormGearMeshModalAnalysesAtStiffnesses]':
        '''List[WormGearMeshModalAnalysesAtStiffnesses]: 'ConnectionModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtStiffnessesLoadCases, constructor.new(_3839.WormGearMeshModalAnalysesAtStiffnesses))
        return value
