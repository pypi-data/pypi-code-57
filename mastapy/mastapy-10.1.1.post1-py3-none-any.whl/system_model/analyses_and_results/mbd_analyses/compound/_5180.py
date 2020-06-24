'''_5180.py

MassDiscCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2004
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5043
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5225
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'MassDiscCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundMultiBodyDynamicsAnalysis',)


class MassDiscCompoundMultiBodyDynamicsAnalysis(_5225.VirtualComponentCompoundMultiBodyDynamicsAnalysis):
    '''MassDiscCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2004.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5043.MassDiscMultiBodyDynamicsAnalysis]':
        '''List[MassDiscMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5043.MassDiscMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5043.MassDiscMultiBodyDynamicsAnalysis]':
        '''List[MassDiscMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5043.MassDiscMultiBodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundMultiBodyDynamicsAnalysis]':
        '''List[MassDiscCompoundMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundMultiBodyDynamicsAnalysis))
        return value
