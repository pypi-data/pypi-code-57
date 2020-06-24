'''_4133.py

CylindricalGearMeshCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1870
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4007
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4143
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'CylindricalGearMeshCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundModalAnalysesAtSpeeds',)


class CylindricalGearMeshCompoundModalAnalysesAtSpeeds(_4143.GearMeshCompoundModalAnalysesAtSpeeds):
    '''CylindricalGearMeshCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1870.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1870.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1870.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1870.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4007.CylindricalGearMeshModalAnalysesAtSpeeds]':
        '''List[CylindricalGearMeshModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4007.CylindricalGearMeshModalAnalysesAtSpeeds))
        return value

    @property
    def connection_modal_analyses_at_speeds_load_cases(self) -> 'List[_4007.CylindricalGearMeshModalAnalysesAtSpeeds]':
        '''List[CylindricalGearMeshModalAnalysesAtSpeeds]: 'ConnectionModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtSpeedsLoadCases, constructor.new(_4007.CylindricalGearMeshModalAnalysesAtSpeeds))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[CylindricalGearMeshCompoundModalAnalysesAtSpeeds]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundModalAnalysesAtSpeeds))
        return value
