'''_3037.py

RollingRingAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2042
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2249
from mastapy.system_model.analyses_and_results.system_deflections import _2229
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3032
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'RollingRingAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAdvancedSystemDeflection',)


class RollingRingAdvancedSystemDeflection(_3032.CouplingHalfAdvancedSystemDeflection):
    '''RollingRingAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2042.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2042.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2249.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2249.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingAdvancedSystemDeflection]':
        '''List[RollingRingAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingAdvancedSystemDeflection))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2229.RollingRingSystemDeflection]':
        '''List[RollingRingSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2229.RollingRingSystemDeflection))
        return value
