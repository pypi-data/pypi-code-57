'''_3499.py

BoltedJointCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _1911
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4149
from mastapy.system_model.analyses_and_results.power_flows.compound import _3516
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BoltedJointCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundPowerFlow',)


class BoltedJointCompoundPowerFlow(_3516.SpecialisedAssemblyCompoundPowerFlow):
    '''BoltedJointCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4149.BoltedJointPowerFlow]':
        '''List[BoltedJointPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4149.BoltedJointPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_4149.BoltedJointPowerFlow]':
        '''List[BoltedJointPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_4149.BoltedJointPowerFlow))
        return value
