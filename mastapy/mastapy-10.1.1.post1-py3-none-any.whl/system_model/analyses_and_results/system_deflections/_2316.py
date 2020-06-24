'''_2316.py

SpringDamperSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2133
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6183
from mastapy.system_model.analyses_and_results.power_flows import _3315
from mastapy.system_model.analyses_and_results.system_deflections import _2246
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SpringDamperSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperSystemDeflection',)


class SpringDamperSystemDeflection(_2246.CouplingSystemDeflection):
    '''SpringDamperSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2133.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6183.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6183.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3315.SpringDamperPowerFlow':
        '''SpringDamperPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3315.SpringDamperPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
