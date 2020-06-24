'''_6380.py

ClutchConnectionCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1894
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6255
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6396
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ClutchConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundAdvancedSystemDeflection',)


class ClutchConnectionCompoundAdvancedSystemDeflection(_6396.CouplingConnectionCompoundAdvancedSystemDeflection):
    '''ClutchConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1894.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1894.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6255.ClutchConnectionAdvancedSystemDeflection]':
        '''List[ClutchConnectionAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6255.ClutchConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_advanced_system_deflection_load_cases(self) -> 'List[_6255.ClutchConnectionAdvancedSystemDeflection]':
        '''List[ClutchConnectionAdvancedSystemDeflection]: 'ConnectionAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedSystemDeflectionLoadCases, constructor.new(_6255.ClutchConnectionAdvancedSystemDeflection))
        return value
