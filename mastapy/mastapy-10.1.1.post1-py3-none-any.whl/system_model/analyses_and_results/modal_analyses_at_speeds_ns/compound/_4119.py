'''_4119.py

ConceptGearMeshCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1866
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3993
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4143
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ConceptGearMeshCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundModalAnalysesAtSpeeds',)


class ConceptGearMeshCompoundModalAnalysesAtSpeeds(_4143.GearMeshCompoundModalAnalysesAtSpeeds):
    '''ConceptGearMeshCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1866.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1866.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1866.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1866.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3993.ConceptGearMeshModalAnalysesAtSpeeds]':
        '''List[ConceptGearMeshModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3993.ConceptGearMeshModalAnalysesAtSpeeds))
        return value

    @property
    def connection_modal_analyses_at_speeds_load_cases(self) -> 'List[_3993.ConceptGearMeshModalAnalysesAtSpeeds]':
        '''List[ConceptGearMeshModalAnalysesAtSpeeds]: 'ConnectionModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtSpeedsLoadCases, constructor.new(_3993.ConceptGearMeshModalAnalysesAtSpeeds))
        return value
