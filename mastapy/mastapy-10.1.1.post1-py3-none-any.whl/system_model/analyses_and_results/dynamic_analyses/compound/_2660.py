'''_2660.py

BoltedJointCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1911
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3677
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2678
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'BoltedJointCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundDynamicAnalysis',)


class BoltedJointCompoundDynamicAnalysis(_2678.SpecialisedAssemblyCompoundDynamicAnalysis):
    '''BoltedJointCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3677.BoltedJointDynamicAnalysis]':
        '''List[BoltedJointDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3677.BoltedJointDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3677.BoltedJointDynamicAnalysis]':
        '''List[BoltedJointDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3677.BoltedJointDynamicAnalysis))
        return value
