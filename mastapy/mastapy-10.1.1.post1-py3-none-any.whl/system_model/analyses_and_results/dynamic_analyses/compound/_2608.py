'''_2608.py

SpringDamperCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1998
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3634
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2600
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'SpringDamperCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundDynamicAnalysis',)


class SpringDamperCompoundDynamicAnalysis(_2600.CouplingCompoundDynamicAnalysis):
    '''SpringDamperCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1998.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1998.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3634.SpringDamperDynamicAnalysis]':
        '''List[SpringDamperDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3634.SpringDamperDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3634.SpringDamperDynamicAnalysis]':
        '''List[SpringDamperDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3634.SpringDamperDynamicAnalysis))
        return value
