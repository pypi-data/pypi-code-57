'''_5802.py

BeltConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1832
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6055
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5856
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'BeltConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionDynamicAnalysis',)


class BeltConnectionDynamicAnalysis(_5856.InterMountableComponentConnectionDynamicAnalysis):
    '''BeltConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1832.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6055.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6055.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
