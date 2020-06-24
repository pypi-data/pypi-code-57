'''_3165.py

ConceptGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _1994
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4200
from mastapy.system_model.analyses_and_results.power_flows.compound import _3182
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConceptGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundPowerFlow',)


class ConceptGearCompoundPowerFlow(_3182.GearCompoundPowerFlow):
    '''ConceptGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1994.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4200.ConceptGearPowerFlow]':
        '''List[ConceptGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4200.ConceptGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_4200.ConceptGearPowerFlow]':
        '''List[ConceptGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_4200.ConceptGearPowerFlow))
        return value
