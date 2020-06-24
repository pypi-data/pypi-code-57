'''_3641.py

CylindricalGearCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2064
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3505
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3651
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CylindricalGearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundParametricStudyTool',)


class CylindricalGearCompoundParametricStudyTool(_3651.GearCompoundParametricStudyTool):
    '''CylindricalGearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2064.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3505.CylindricalGearParametricStudyTool]':
        '''List[CylindricalGearParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3505.CylindricalGearParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3505.CylindricalGearParametricStudyTool]':
        '''List[CylindricalGearParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3505.CylindricalGearParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundParametricStudyTool]':
        '''List[CylindricalGearCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundParametricStudyTool))
        return value
