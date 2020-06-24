'''_3250.py

SpiralBevelGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2002
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4081
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3232
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'SpiralBevelGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearCompoundParametricStudyTool',)


class SpiralBevelGearCompoundParametricStudyTool(_3232.BevelGearCompoundParametricStudyTool):
    '''SpiralBevelGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2002.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2002.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4081.SpiralBevelGearParametricStudyTool]':
        '''List[SpiralBevelGearParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4081.SpiralBevelGearParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4081.SpiralBevelGearParametricStudyTool]':
        '''List[SpiralBevelGearParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4081.SpiralBevelGearParametricStudyTool))
        return value
