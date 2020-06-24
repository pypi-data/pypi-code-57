'''_3107.py

TorqueConverterCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1991
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3877
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3093
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'TorqueConverterCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundModalAnalysis',)


class TorqueConverterCompoundModalAnalysis(_3093.CouplingCompoundModalAnalysis):
    '''TorqueConverterCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1991.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1991.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3877.TorqueConverterModalAnalysis]':
        '''List[TorqueConverterModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3877.TorqueConverterModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3877.TorqueConverterModalAnalysis]':
        '''List[TorqueConverterModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3877.TorqueConverterModalAnalysis))
        return value
