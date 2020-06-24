'''_5165.py

ZerolBevelGearMeshCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1820
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5044
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5062
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'ZerolBevelGearMeshCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCompoundModalAnalysesAtStiffnesses',)


class ZerolBevelGearMeshCompoundModalAnalysesAtStiffnesses(_5062.BevelGearMeshCompoundModalAnalysesAtStiffnesses):
    '''ZerolBevelGearMeshCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1820.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1820.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1820.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1820.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5044.ZerolBevelGearMeshModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearMeshModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5044.ZerolBevelGearMeshModalAnalysesAtStiffnesses))
        return value

    @property
    def connection_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_5044.ZerolBevelGearMeshModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearMeshModalAnalysesAtStiffnesses]: 'ConnectionModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtStiffnessesLoadCases, constructor.new(_5044.ZerolBevelGearMeshModalAnalysesAtStiffnesses))
        return value
