'''_3576.py

RootAssemblyCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools import _4916
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5014, _5015, _2058, _2056,
    _4922
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3565
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'RootAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundParametricStudyTool',)


class RootAssemblyCompoundParametricStudyTool(_3565.AssemblyCompoundParametricStudyTool):
    '''RootAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def parametric_analysis_options(self) -> '_4916.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4916.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def compound_load_case(self) -> '_5014.AbstractLoadCaseGroup':
        '''AbstractLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5014.AbstractLoadCaseGroup)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_group_of_time_series_load_cases(self) -> '_5015.GroupOfTimeSeriesLoadCases':
        '''GroupOfTimeSeriesLoadCases: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundLoadCase.__class__.__qualname__ != 'GroupOfTimeSeriesLoadCases':
            raise CastException('Failed to cast compound_load_case to GroupOfTimeSeriesLoadCases. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5015.GroupOfTimeSeriesLoadCases)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_duty_cycle(self) -> '_2058.DutyCycle':
        '''DutyCycle: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundLoadCase.__class__.__qualname__ != 'DutyCycle':
            raise CastException('Failed to cast compound_load_case to DutyCycle. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_2058.DutyCycle)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_design_state(self) -> '_2056.DesignState':
        '''DesignState: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundLoadCase.__class__.__qualname__ != 'DesignState':
            raise CastException('Failed to cast compound_load_case to DesignState. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_2056.DesignState)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_sub_group_in_single_design_state(self) -> '_4922.SubGroupInSingleDesignState':
        '''SubGroupInSingleDesignState: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundLoadCase.__class__.__qualname__ != 'SubGroupInSingleDesignState':
            raise CastException('Failed to cast compound_load_case to SubGroupInSingleDesignState. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_4922.SubGroupInSingleDesignState)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None
