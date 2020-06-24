'''_5014.py

AbstractLoadCaseGroup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model import _1719
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4916
from mastapy.system_model.analyses_and_results.static_loads import _2299, _6181, _4919
from mastapy.system_model.analyses_and_results import (
    _2133, _2128, _2113, _2120,
    _2127, _2130, _2131, _2132,
    _2125, _2115, _2124, _2123,
    _2121, _2122, _2134, _2129,
    _2114, _2118, _2117, _2116,
    _2119, _2126, _2080
)
from mastapy import _320, _1
from mastapy._internal.python_net import python_net_import

_ABSTRACT_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractLoadCaseGroup',)


class AbstractLoadCaseGroup(_1.APIBase):
    '''AbstractLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_LOAD_CASE_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def total_duration(self) -> 'float':
        '''float: 'TotalDuration' is the original name of this property.'''

        return self.wrapped.TotalDuration

    @total_duration.setter
    def total_duration(self, value: 'float'):
        self.wrapped.TotalDuration = float(value) if value else 0.0

    @property
    def model(self) -> '_1719.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1719.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def parametric_analysis_options(self) -> '_4916.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4916.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def load_case_root_assemblies(self) -> 'List[_2299.RootAssemblyLoadCase]':
        '''List[RootAssemblyLoadCase]: 'LoadCaseRootAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseRootAssemblies, constructor.new(_2299.RootAssemblyLoadCase))
        return value

    @property
    def compound_system_deflection(self) -> '_2133.CompoundSystemDeflectionAnalysis':
        '''CompoundSystemDeflectionAnalysis: 'CompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.CompoundSystemDeflectionAnalysis)(self.wrapped.CompoundSystemDeflection) if self.wrapped.CompoundSystemDeflection else None

    @property
    def compound_power_flow(self) -> '_2128.CompoundPowerFlowAnalysis':
        '''CompoundPowerFlowAnalysis: 'CompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.CompoundPowerFlowAnalysis)(self.wrapped.CompoundPowerFlow) if self.wrapped.CompoundPowerFlow else None

    @property
    def compound_advanced_system_deflection(self) -> '_2113.CompoundAdvancedSystemDeflectionAnalysis':
        '''CompoundAdvancedSystemDeflectionAnalysis: 'CompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2113.CompoundAdvancedSystemDeflectionAnalysis)(self.wrapped.CompoundAdvancedSystemDeflection) if self.wrapped.CompoundAdvancedSystemDeflection else None

    @property
    def compound_gear_whine_analysis(self) -> '_2120.CompoundGearWhineAnalysisAnalysis':
        '''CompoundGearWhineAnalysisAnalysis: 'CompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.CompoundGearWhineAnalysisAnalysis)(self.wrapped.CompoundGearWhineAnalysis) if self.wrapped.CompoundGearWhineAnalysis else None

    @property
    def compound_multibody_dynamics(self) -> '_2127.CompoundMultibodyDynamicsAnalysis':
        '''CompoundMultibodyDynamicsAnalysis: 'CompoundMultibodyDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2127.CompoundMultibodyDynamicsAnalysis)(self.wrapped.CompoundMultibodyDynamics) if self.wrapped.CompoundMultibodyDynamics else None

    @property
    def compound_steady_state_synchronous_response(self) -> '_2130.CompoundSteadyStateSynchronousResponseAnalysis':
        '''CompoundSteadyStateSynchronousResponseAnalysis: 'CompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.CompoundSteadyStateSynchronousResponseAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponse) if self.wrapped.CompoundSteadyStateSynchronousResponse else None

    @property
    def compound_steady_state_synchronous_responseata_speed(self) -> '_2131.CompoundSteadyStateSynchronousResponseataSpeedAnalysis':
        '''CompoundSteadyStateSynchronousResponseataSpeedAnalysis: 'CompoundSteadyStateSynchronousResponseataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.CompoundSteadyStateSynchronousResponseataSpeedAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponseataSpeed) if self.wrapped.CompoundSteadyStateSynchronousResponseataSpeed else None

    @property
    def compound_steady_state_synchronous_responseona_shaft(self) -> '_2132.CompoundSteadyStateSynchronousResponseonaShaftAnalysis':
        '''CompoundSteadyStateSynchronousResponseonaShaftAnalysis: 'CompoundSteadyStateSynchronousResponseonaShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.CompoundSteadyStateSynchronousResponseonaShaftAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponseonaShaft) if self.wrapped.CompoundSteadyStateSynchronousResponseonaShaft else None

    @property
    def compound_modal_analysis(self) -> '_2125.CompoundModalAnalysisAnalysis':
        '''CompoundModalAnalysisAnalysis: 'CompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2125.CompoundModalAnalysisAnalysis)(self.wrapped.CompoundModalAnalysis) if self.wrapped.CompoundModalAnalysis else None

    @property
    def compound_dynamic_analysis(self) -> '_2115.CompoundDynamicAnalysisAnalysis':
        '''CompoundDynamicAnalysisAnalysis: 'CompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2115.CompoundDynamicAnalysisAnalysis)(self.wrapped.CompoundDynamicAnalysis) if self.wrapped.CompoundDynamicAnalysis else None

    @property
    def compound_modal_analysesat_stiffnesses(self) -> '_2124.CompoundModalAnalysesatStiffnessesAnalysis':
        '''CompoundModalAnalysesatStiffnessesAnalysis: 'CompoundModalAnalysesatStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2124.CompoundModalAnalysesatStiffnessesAnalysis)(self.wrapped.CompoundModalAnalysesatStiffnesses) if self.wrapped.CompoundModalAnalysesatStiffnesses else None

    @property
    def compound_modal_analysesat_speeds(self) -> '_2123.CompoundModalAnalysesatSpeedsAnalysis':
        '''CompoundModalAnalysesatSpeedsAnalysis: 'CompoundModalAnalysesatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2123.CompoundModalAnalysesatSpeedsAnalysis)(self.wrapped.CompoundModalAnalysesatSpeeds) if self.wrapped.CompoundModalAnalysesatSpeeds else None

    @property
    def compound_modal_analysesata_speed(self) -> '_2121.CompoundModalAnalysesataSpeedAnalysis':
        '''CompoundModalAnalysesataSpeedAnalysis: 'CompoundModalAnalysesataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.CompoundModalAnalysesataSpeedAnalysis)(self.wrapped.CompoundModalAnalysesataSpeed) if self.wrapped.CompoundModalAnalysesataSpeed else None

    @property
    def compound_modal_analysesata_stiffness(self) -> '_2122.CompoundModalAnalysesataStiffnessAnalysis':
        '''CompoundModalAnalysesataStiffnessAnalysis: 'CompoundModalAnalysesataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.CompoundModalAnalysesataStiffnessAnalysis)(self.wrapped.CompoundModalAnalysesataStiffness) if self.wrapped.CompoundModalAnalysesataStiffness else None

    @property
    def compound_torsional_system_deflection(self) -> '_2134.CompoundTorsionalSystemDeflectionAnalysis':
        '''CompoundTorsionalSystemDeflectionAnalysis: 'CompoundTorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.CompoundTorsionalSystemDeflectionAnalysis)(self.wrapped.CompoundTorsionalSystemDeflection) if self.wrapped.CompoundTorsionalSystemDeflection else None

    @property
    def compound_single_mesh_whine_analysis(self) -> '_2129.CompoundSingleMeshWhineAnalysisAnalysis':
        '''CompoundSingleMeshWhineAnalysisAnalysis: 'CompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2129.CompoundSingleMeshWhineAnalysisAnalysis)(self.wrapped.CompoundSingleMeshWhineAnalysis) if self.wrapped.CompoundSingleMeshWhineAnalysis else None

    @property
    def compound_advanced_system_deflection_sub_analysis(self) -> '_2114.CompoundAdvancedSystemDeflectionSubAnalysisAnalysis':
        '''CompoundAdvancedSystemDeflectionSubAnalysisAnalysis: 'CompoundAdvancedSystemDeflectionSubAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.CompoundAdvancedSystemDeflectionSubAnalysisAnalysis)(self.wrapped.CompoundAdvancedSystemDeflectionSubAnalysis) if self.wrapped.CompoundAdvancedSystemDeflectionSubAnalysis else None

    @property
    def compound_dynamic_modelfor_gear_whine(self) -> '_2118.CompoundDynamicModelforGearWhineAnalysis':
        '''CompoundDynamicModelforGearWhineAnalysis: 'CompoundDynamicModelforGearWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2118.CompoundDynamicModelforGearWhineAnalysis)(self.wrapped.CompoundDynamicModelforGearWhine) if self.wrapped.CompoundDynamicModelforGearWhine else None

    @property
    def compound_dynamic_modelforat_speeds(self) -> '_2117.CompoundDynamicModelforatSpeedsAnalysis':
        '''CompoundDynamicModelforatSpeedsAnalysis: 'CompoundDynamicModelforatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.CompoundDynamicModelforatSpeedsAnalysis)(self.wrapped.CompoundDynamicModelforatSpeeds) if self.wrapped.CompoundDynamicModelforatSpeeds else None

    @property
    def compound_dynamic_modelata_stiffness(self) -> '_2116.CompoundDynamicModelataStiffnessAnalysis':
        '''CompoundDynamicModelataStiffnessAnalysis: 'CompoundDynamicModelataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.CompoundDynamicModelataStiffnessAnalysis)(self.wrapped.CompoundDynamicModelataStiffness) if self.wrapped.CompoundDynamicModelataStiffness else None

    @property
    def compound_dynamic_modelfor_steady_state_synchronous_response(self) -> '_2119.CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis':
        '''CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis: 'CompoundDynamicModelforSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis)(self.wrapped.CompoundDynamicModelforSteadyStateSynchronousResponse) if self.wrapped.CompoundDynamicModelforSteadyStateSynchronousResponse else None

    @property
    def compound_modal_analysisfor_whine(self) -> '_2126.CompoundModalAnalysisforWhineAnalysis':
        '''CompoundModalAnalysisforWhineAnalysis: 'CompoundModalAnalysisforWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.CompoundModalAnalysisforWhineAnalysis)(self.wrapped.CompoundModalAnalysisforWhine) if self.wrapped.CompoundModalAnalysisforWhine else None

    def create_load_cases(self, number_of_load_cases: 'int', token: '_320.TaskProgress') -> 'List[_6181.LoadCase]':
        ''' 'CreateLoadCases' is the original name of this method.

        Args:
            number_of_load_cases (int)
            token (mastapy.TaskProgress)

        Returns:
            List[mastapy.system_model.analyses_and_results.static_loads.LoadCase]
        '''

        number_of_load_cases = int(number_of_load_cases)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.CreateLoadCases(number_of_load_cases if number_of_load_cases else 0, token.wrapped if token else None), constructor.new(_6181.LoadCase))

    def analysis_of(self, analysis_type: '_4919.AnalysisType') -> '_2080.CompoundAnalysis':
        ''' 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.CompoundAnalysis
        '''

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        return constructor.new(_2080.CompoundAnalysis)(method_result) if method_result else None
