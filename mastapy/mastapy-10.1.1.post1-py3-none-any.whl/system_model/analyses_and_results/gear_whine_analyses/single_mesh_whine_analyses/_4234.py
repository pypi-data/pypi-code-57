'''_4234.py

BeltConnectionSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1760
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2213
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4237
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BeltConnectionSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionSingleMeshWhineAnalysis',)


class BeltConnectionSingleMeshWhineAnalysis(_4237.InterMountableComponentConnectionSingleMeshWhineAnalysis):
    '''BeltConnectionSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1760.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2213.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2213.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
