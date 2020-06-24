'''_3563.py

RollingRingConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1852
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6170
from mastapy.system_model.analyses_and_results.system_deflections import _2302
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3528
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'RollingRingConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionParametricStudyTool',)


class RollingRingConnectionParametricStudyTool(_3528.InterMountableComponentConnectionParametricStudyTool):
    '''RollingRingConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1852.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1852.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6170.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6170.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionParametricStudyTool]':
        '''List[RollingRingConnectionParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionParametricStudyTool))
        return value

    @property
    def connection_system_deflection_results(self) -> 'List[_2302.RollingRingConnectionSystemDeflection]':
        '''List[RollingRingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2302.RollingRingConnectionSystemDeflection))
        return value
