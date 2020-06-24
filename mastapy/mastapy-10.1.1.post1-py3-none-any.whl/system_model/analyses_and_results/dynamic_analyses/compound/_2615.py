'''_2615.py

TorqueConverterPumpCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2030
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3641
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2601
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'TorqueConverterPumpCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundDynamicAnalysis',)


class TorqueConverterPumpCompoundDynamicAnalysis(_2601.CouplingHalfCompoundDynamicAnalysis):
    '''TorqueConverterPumpCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2030.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2030.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3641.TorqueConverterPumpDynamicAnalysis]':
        '''List[TorqueConverterPumpDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3641.TorqueConverterPumpDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_3641.TorqueConverterPumpDynamicAnalysis]':
        '''List[TorqueConverterPumpDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_3641.TorqueConverterPumpDynamicAnalysis))
        return value
