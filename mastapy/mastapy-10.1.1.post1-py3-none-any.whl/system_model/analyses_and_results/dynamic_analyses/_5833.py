'''_5833.py

CVTBeltConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1837
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5802
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CVTBeltConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionDynamicAnalysis',)


class CVTBeltConnectionDynamicAnalysis(_5802.BeltConnectionDynamicAnalysis):
    '''CVTBeltConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1837.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1837.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
