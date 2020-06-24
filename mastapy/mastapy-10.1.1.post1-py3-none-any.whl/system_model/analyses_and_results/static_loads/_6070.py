'''_6070.py

CoaxialConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets import _1833
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6175
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CoaxialConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionLoadCase',)


class CoaxialConnectionLoadCase(_6175.ShaftToMountableComponentConnectionLoadCase):
    '''CoaxialConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
