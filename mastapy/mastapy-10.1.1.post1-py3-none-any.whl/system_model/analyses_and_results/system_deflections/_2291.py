'''_2291.py

OilSealSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2008
from mastapy.system_model.analyses_and_results.static_loads import _6153
from mastapy.system_model.analyses_and_results.power_flows import _3289
from mastapy.system_model.analyses_and_results.system_deflections import _2243
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'OilSealSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSystemDeflection',)


class OilSealSystemDeflection(_2243.ConnectorSystemDeflection):
    '''OilSealSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def reliability_for_oil_seal(self) -> 'float':
        '''float: 'ReliabilityForOilSeal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReliabilityForOilSeal

    @property
    def component_design(self) -> '_2008.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2008.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6153.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6153.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3289.OilSealPowerFlow':
        '''OilSealPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3289.OilSealPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
