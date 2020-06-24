'''_2160.py

ConceptCouplingConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _1824
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2226
from mastapy.system_model.analyses_and_results.system_deflections import _2227
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptCouplingConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionSystemDeflection',)


class ConceptCouplingConnectionSystemDeflection(_2227.CouplingConnectionSystemDeflection):
    '''ConceptCouplingConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1824.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1824.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2226.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2226.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
