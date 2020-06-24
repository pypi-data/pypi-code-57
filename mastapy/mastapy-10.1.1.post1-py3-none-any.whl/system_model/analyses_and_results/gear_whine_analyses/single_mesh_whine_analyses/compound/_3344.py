'''_3344.py

TorqueConverterTurbineCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2022
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4303
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _3329
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'TorqueConverterTurbineCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundSingleMeshWhineAnalysis',)


class TorqueConverterTurbineCompoundSingleMeshWhineAnalysis(_3329.CouplingHalfCompoundSingleMeshWhineAnalysis):
    '''TorqueConverterTurbineCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2022.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4303.TorqueConverterTurbineSingleMeshWhineAnalysis]':
        '''List[TorqueConverterTurbineSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4303.TorqueConverterTurbineSingleMeshWhineAnalysis))
        return value

    @property
    def component_single_mesh_whine_analysis_load_cases(self) -> 'List[_4303.TorqueConverterTurbineSingleMeshWhineAnalysis]':
        '''List[TorqueConverterTurbineSingleMeshWhineAnalysis]: 'ComponentSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSingleMeshWhineAnalysisLoadCases, constructor.new(_4303.TorqueConverterTurbineSingleMeshWhineAnalysis))
        return value
