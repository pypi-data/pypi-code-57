'''_3503.py

ExternalCADModelCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _1919
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4153
from mastapy.system_model.analyses_and_results.power_flows.compound import _3500
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ExternalCADModelCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelCompoundPowerFlow',)


class ExternalCADModelCompoundPowerFlow(_3500.ComponentCompoundPowerFlow):
    '''ExternalCADModelCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4153.ExternalCADModelPowerFlow]':
        '''List[ExternalCADModelPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4153.ExternalCADModelPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4153.ExternalCADModelPowerFlow]':
        '''List[ExternalCADModelPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4153.ExternalCADModelPowerFlow))
        return value
