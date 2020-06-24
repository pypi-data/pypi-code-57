'''_3537.py

TorqueConverterConnectionCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1830
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4012
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3535
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'TorqueConverterConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundParametricStudyTool',)


class TorqueConverterConnectionCompoundParametricStudyTool(_3535.CouplingConnectionCompoundParametricStudyTool):
    '''TorqueConverterConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4012.TorqueConverterConnectionParametricStudyTool]':
        '''List[TorqueConverterConnectionParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4012.TorqueConverterConnectionParametricStudyTool))
        return value

    @property
    def connection_parametric_study_tool_load_cases(self) -> 'List[_4012.TorqueConverterConnectionParametricStudyTool]':
        '''List[TorqueConverterConnectionParametricStudyTool]: 'ConnectionParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionParametricStudyToolLoadCases, constructor.new(_4012.TorqueConverterConnectionParametricStudyTool))
        return value
