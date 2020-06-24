'''_5169.py

ImportedFEComponentCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2001
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5028
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5112
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ImportedFEComponentCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundMultiBodyDynamicsAnalysis',)


class ImportedFEComponentCompoundMultiBodyDynamicsAnalysis(_5112.AbstractShaftOrHousingCompoundMultiBodyDynamicsAnalysis):
    '''ImportedFEComponentCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5028.ImportedFEComponentMultiBodyDynamicsAnalysis]':
        '''List[ImportedFEComponentMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5028.ImportedFEComponentMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5028.ImportedFEComponentMultiBodyDynamicsAnalysis]':
        '''List[ImportedFEComponentMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5028.ImportedFEComponentMultiBodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ImportedFEComponentCompoundMultiBodyDynamicsAnalysis]':
        '''List[ImportedFEComponentCompoundMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentCompoundMultiBodyDynamicsAnalysis))
        return value
