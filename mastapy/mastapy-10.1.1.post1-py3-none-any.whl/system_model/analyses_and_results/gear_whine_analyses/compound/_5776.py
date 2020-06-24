'''_5776.py

TorqueConverterPumpCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2141
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5387
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5702
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'TorqueConverterPumpCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundGearWhineAnalysis',)


class TorqueConverterPumpCompoundGearWhineAnalysis(_5702.CouplingHalfCompoundGearWhineAnalysis):
    '''TorqueConverterPumpCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2141.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5387.TorqueConverterPumpGearWhineAnalysis]':
        '''List[TorqueConverterPumpGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5387.TorqueConverterPumpGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5387.TorqueConverterPumpGearWhineAnalysis]':
        '''List[TorqueConverterPumpGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5387.TorqueConverterPumpGearWhineAnalysis))
        return value
