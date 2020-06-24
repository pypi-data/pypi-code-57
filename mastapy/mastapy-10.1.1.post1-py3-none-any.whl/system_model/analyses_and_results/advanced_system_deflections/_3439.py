'''_3439.py

BearingAdvancedSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results import _1521
from mastapy.system_model.part_model import _1908
from mastapy.system_model.analyses_and_results.static_loads import _2265
from mastapy.system_model.analyses_and_results.system_deflections import _2141
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3443
from mastapy._internal.python_net import python_net_import

_BEARING_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BearingAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingAdvancedSystemDeflection',)


class BearingAdvancedSystemDeflection(_3443.ConnectorAdvancedSystemDeflection):
    '''BearingAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEARING_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_variable_stiffness(self) -> 'bool':
        '''bool: 'UseVariableStiffness' is the original name of this property.'''

        return self.wrapped.UseVariableStiffness

    @use_variable_stiffness.setter
    def use_variable_stiffness(self, value: 'bool'):
        self.wrapped.UseVariableStiffness = bool(value) if value else False

    @property
    def duty_cycle(self) -> '_1521.LoadedBearingDutyCycle':
        '''LoadedBearingDutyCycle: 'DutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1521.LoadedBearingDutyCycle)(self.wrapped.DutyCycle) if self.wrapped.DutyCycle else None

    @property
    def component_design(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2265.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2265.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingAdvancedSystemDeflection))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2141.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2141.BearingSystemDeflection))
        return value
