'''_3622.py

CoaxialConnectionCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1833
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3485
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3689
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CoaxialConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionCompoundParametricStudyTool',)


class CoaxialConnectionCompoundParametricStudyTool(_3689.ShaftToMountableComponentConnectionCompoundParametricStudyTool):
    '''CoaxialConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3485.CoaxialConnectionParametricStudyTool]':
        '''List[CoaxialConnectionParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3485.CoaxialConnectionParametricStudyTool))
        return value

    @property
    def connection_parametric_study_tool_load_cases(self) -> 'List[_3485.CoaxialConnectionParametricStudyTool]':
        '''List[CoaxialConnectionParametricStudyTool]: 'ConnectionParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionParametricStudyToolLoadCases, constructor.new(_3485.CoaxialConnectionParametricStudyTool))
        return value
