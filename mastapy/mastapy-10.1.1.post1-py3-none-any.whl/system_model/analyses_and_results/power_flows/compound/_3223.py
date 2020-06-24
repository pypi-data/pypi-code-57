'''_3223.py

SynchroniserSleeveCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2025
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4140
from mastapy.system_model.analyses_and_results.power_flows.compound import _3222
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SynchroniserSleeveCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveCompoundPowerFlow',)


class SynchroniserSleeveCompoundPowerFlow(_3222.SynchroniserPartCompoundPowerFlow):
    '''SynchroniserSleeveCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4140.SynchroniserSleevePowerFlow]':
        '''List[SynchroniserSleevePowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4140.SynchroniserSleevePowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4140.SynchroniserSleevePowerFlow]':
        '''List[SynchroniserSleevePowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4140.SynchroniserSleevePowerFlow))
        return value
