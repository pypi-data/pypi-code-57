'''_3404.py

TorqueConverterAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1991
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2206
from mastapy.system_model.analyses_and_results.system_deflections import _2205
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3390
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'TorqueConverterAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterAdvancedSystemDeflection',)


class TorqueConverterAdvancedSystemDeflection(_3390.CouplingAdvancedSystemDeflection):
    '''TorqueConverterAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1991.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2206.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2205.TorqueConverterSystemDeflection]':
        '''List[TorqueConverterSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2205.TorqueConverterSystemDeflection))
        return value
