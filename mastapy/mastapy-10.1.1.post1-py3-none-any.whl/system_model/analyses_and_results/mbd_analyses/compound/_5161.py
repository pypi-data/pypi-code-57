'''_5161.py

FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1997
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5019
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5201
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis',)


class FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis(_5201.SpecialisedAssemblyCompoundMultiBodyDynamicsAnalysis):
    '''FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyCompoundMultiBodyDynamicsAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5019.FlexiblePinAssemblyMultiBodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5019.FlexiblePinAssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5019.FlexiblePinAssemblyMultiBodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5019.FlexiblePinAssemblyMultiBodyDynamicsAnalysis))
        return value
