'''_3697.py

StraightBevelDiffGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2084
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3577
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3614
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'StraightBevelDiffGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundParametricStudyTool',)


class StraightBevelDiffGearCompoundParametricStudyTool(_3614.BevelGearCompoundParametricStudyTool):
    '''StraightBevelDiffGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2084.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2084.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3577.StraightBevelDiffGearParametricStudyTool]':
        '''List[StraightBevelDiffGearParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3577.StraightBevelDiffGearParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3577.StraightBevelDiffGearParametricStudyTool]':
        '''List[StraightBevelDiffGearParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3577.StraightBevelDiffGearParametricStudyTool))
        return value
