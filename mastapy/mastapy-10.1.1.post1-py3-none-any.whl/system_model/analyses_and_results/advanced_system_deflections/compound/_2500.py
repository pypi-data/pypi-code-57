'''_2500.py

BeltConnectionCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1760
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3408
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2503
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BeltConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionCompoundAdvancedSystemDeflection',)


class BeltConnectionCompoundAdvancedSystemDeflection(_2503.InterMountableComponentConnectionCompoundAdvancedSystemDeflection):
    '''BeltConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionCompoundAdvancedSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3408.BeltConnectionAdvancedSystemDeflection]':
        '''List[BeltConnectionAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3408.BeltConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_advanced_system_deflection_load_cases(self) -> 'List[_3408.BeltConnectionAdvancedSystemDeflection]':
        '''List[BeltConnectionAdvancedSystemDeflection]: 'ConnectionAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedSystemDeflectionLoadCases, constructor.new(_3408.BeltConnectionAdvancedSystemDeflection))
        return value
