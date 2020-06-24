'''_2154.py

ClutchConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _1822
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2225
from mastapy.system_model.analyses_and_results.system_deflections import _2227
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionSystemDeflection',)


class ClutchConnectionSystemDeflection(_2227.CouplingConnectionSystemDeflection):
    '''ClutchConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1822.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1822.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2225.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
