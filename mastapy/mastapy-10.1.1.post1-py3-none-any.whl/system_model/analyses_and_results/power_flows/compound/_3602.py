'''_3602.py

CylindricalGearMeshCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4135
from mastapy.system_model.analyses_and_results.power_flows.compound import _3611
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CylindricalGearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundPowerFlow',)


class CylindricalGearMeshCompoundPowerFlow(_3611.GearMeshCompoundPowerFlow):
    '''CylindricalGearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4135.CylindricalGearMeshPowerFlow]':
        '''List[CylindricalGearMeshPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4135.CylindricalGearMeshPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_4135.CylindricalGearMeshPowerFlow]':
        '''List[CylindricalGearMeshPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_4135.CylindricalGearMeshPowerFlow))
        return value
