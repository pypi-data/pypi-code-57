'''_3576.py

SynchroniserHalfCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2048
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4109
from mastapy.system_model.analyses_and_results.power_flows.compound import _3577
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SynchroniserHalfCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundPowerFlow',)


class SynchroniserHalfCompoundPowerFlow(_3577.SynchroniserPartCompoundPowerFlow):
    '''SynchroniserHalfCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2048.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2048.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4109.SynchroniserHalfPowerFlow]':
        '''List[SynchroniserHalfPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4109.SynchroniserHalfPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4109.SynchroniserHalfPowerFlow]':
        '''List[SynchroniserHalfPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4109.SynchroniserHalfPowerFlow))
        return value
