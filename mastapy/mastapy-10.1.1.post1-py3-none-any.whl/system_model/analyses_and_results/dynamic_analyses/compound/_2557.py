'''_2557.py

FaceGearCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2006
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3701
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2572
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FaceGearCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundDynamicAnalysis',)


class FaceGearCompoundDynamicAnalysis(_2572.GearCompoundDynamicAnalysis):
    '''FaceGearCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2006.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3701.FaceGearDynamicAnalysis]':
        '''List[FaceGearDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3701.FaceGearDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_3701.FaceGearDynamicAnalysis]':
        '''List[FaceGearDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_3701.FaceGearDynamicAnalysis))
        return value
