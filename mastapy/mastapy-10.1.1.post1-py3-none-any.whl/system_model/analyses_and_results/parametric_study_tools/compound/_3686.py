'''_3686.py

RootAssemblyCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools import _3549
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5233, _5232, _5234, _5237,
    _5238, _5240, _5242
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3605
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'RootAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundParametricStudyTool',)


class RootAssemblyCompoundParametricStudyTool(_3605.AssemblyCompoundParametricStudyTool):
    '''RootAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def parametric_analysis_options(self) -> '_3549.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3549.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def compound_load_case(self) -> '_5233.AbstractLoadCaseGroup':
        '''AbstractLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5233.AbstractLoadCaseGroup)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_abstract_design_state_load_case_group(self) -> '_5232.AbstractDesignStateLoadCaseGroup':
        '''AbstractDesignStateLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5232.AbstractDesignStateLoadCaseGroup.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to AbstractDesignStateLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5232.AbstractDesignStateLoadCaseGroup)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_abstract_static_load_case_group(self) -> '_5234.AbstractStaticLoadCaseGroup':
        '''AbstractStaticLoadCaseGroup: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5234.AbstractStaticLoadCaseGroup.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to AbstractStaticLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5234.AbstractStaticLoadCaseGroup)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_design_state(self) -> '_5237.DesignState':
        '''DesignState: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5237.DesignState.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to DesignState. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5237.DesignState)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_duty_cycle(self) -> '_5238.DutyCycle':
        '''DutyCycle: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5238.DutyCycle.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to DutyCycle. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5238.DutyCycle)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_group_of_time_series_load_cases(self) -> '_5240.GroupOfTimeSeriesLoadCases':
        '''GroupOfTimeSeriesLoadCases: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5240.GroupOfTimeSeriesLoadCases.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to GroupOfTimeSeriesLoadCases. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5240.GroupOfTimeSeriesLoadCases)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None

    @property
    def compound_load_case_of_type_sub_group_in_single_design_state(self) -> '_5242.SubGroupInSingleDesignState':
        '''SubGroupInSingleDesignState: 'CompoundLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5242.SubGroupInSingleDesignState.TYPE not in self.wrapped.CompoundLoadCase.__class__.__mro__:
            raise CastException('Failed to cast compound_load_case to SubGroupInSingleDesignState. Expected: {}.'.format(self.wrapped.CompoundLoadCase.__class__.__qualname__))

        return constructor.new(_5242.SubGroupInSingleDesignState)(self.wrapped.CompoundLoadCase) if self.wrapped.CompoundLoadCase else None
