'''_3392.py

FlexiblePinAssemblyCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _1997
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3267
from mastapy.system_model.analyses_and_results.power_flows.compound import _3432
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'FlexiblePinAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyCompoundPowerFlow',)


class FlexiblePinAssemblyCompoundPowerFlow(_3432.SpecialisedAssemblyCompoundPowerFlow):
    '''FlexiblePinAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1997.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3267.FlexiblePinAssemblyPowerFlow]':
        '''List[FlexiblePinAssemblyPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3267.FlexiblePinAssemblyPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3267.FlexiblePinAssemblyPowerFlow]':
        '''List[FlexiblePinAssemblyPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3267.FlexiblePinAssemblyPowerFlow))
        return value
