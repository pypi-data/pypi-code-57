'''_2545.py

ConnectorCompoundAdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2554
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ConnectorCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundAdvancedSystemDeflection',)


class ConnectorCompoundAdvancedSystemDeflection(_2554.MountableComponentCompoundAdvancedSystemDeflection):
    '''ConnectorCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
