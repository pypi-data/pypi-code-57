'''_3526.py

BeltConnectionCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1760
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4001
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3529
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BeltConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundParametricStudyTool',)


class BeltConnectionCompoundParametricStudyTool(_3529.InterMountableComponentConnectionCompoundParametricStudyTool):
    '''BeltConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1760.BeltConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1760.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4001.BeltConnectionParametricStudyTool]':
        '''List[BeltConnectionParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4001.BeltConnectionParametricStudyTool))
        return value

    @property
    def connection_parametric_study_tool_load_cases(self) -> 'List[_4001.BeltConnectionParametricStudyTool]':
        '''List[BeltConnectionParametricStudyTool]: 'ConnectionParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionParametricStudyToolLoadCases, constructor.new(_4001.BeltConnectionParametricStudyTool))
        return value
