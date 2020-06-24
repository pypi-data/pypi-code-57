'''_3560.py

BeltDriveCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2029
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4093
from mastapy.system_model.analyses_and_results.power_flows.compound import _3516
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BeltDriveCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundPowerFlow',)


class BeltDriveCompoundPowerFlow(_3516.SpecialisedAssemblyCompoundPowerFlow):
    '''BeltDriveCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2029.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2029.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4093.BeltDrivePowerFlow]':
        '''List[BeltDrivePowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4093.BeltDrivePowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_4093.BeltDrivePowerFlow]':
        '''List[BeltDrivePowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_4093.BeltDrivePowerFlow))
        return value
