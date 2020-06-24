'''_3094.py

OilSealAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1929
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2323
from mastapy.system_model.analyses_and_results.system_deflections import _2220
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3084
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'OilSealAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealAdvancedSystemDeflection',)


class OilSealAdvancedSystemDeflection(_3084.ConnectorAdvancedSystemDeflection):
    '''OilSealAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1929.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1929.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2323.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2323.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2220.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2220.OilSealSystemDeflection))
        return value
