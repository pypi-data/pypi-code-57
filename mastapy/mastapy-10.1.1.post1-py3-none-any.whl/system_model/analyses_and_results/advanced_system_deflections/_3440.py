'''_3440.py

BoltAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2266
from mastapy.system_model.analyses_and_results.system_deflections import _2153
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3442
from mastapy._internal.python_net import python_net_import

_BOLT_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BoltAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltAdvancedSystemDeflection',)


class BoltAdvancedSystemDeflection(_3442.ComponentAdvancedSystemDeflection):
    '''BoltAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLT_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2266.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2266.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2153.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2153.BoltSystemDeflection))
        return value
