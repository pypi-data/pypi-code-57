'''_2414.py

BoltCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3440
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _2416
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BoltCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundAdvancedSystemDeflection',)


class BoltCompoundAdvancedSystemDeflection(_2416.ComponentCompoundAdvancedSystemDeflection):
    '''BoltCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3440.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3440.BoltAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_3440.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_3440.BoltAdvancedSystemDeflection))
        return value
