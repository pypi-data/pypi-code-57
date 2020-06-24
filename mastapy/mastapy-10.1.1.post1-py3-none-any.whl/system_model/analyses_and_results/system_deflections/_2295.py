'''_2295.py

PartToPartShearCouplingSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2122
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6158
from mastapy.system_model.analyses_and_results.power_flows import _3293
from mastapy.system_model.analyses_and_results.system_deflections import _2246
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PartToPartShearCouplingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingSystemDeflection',)


class PartToPartShearCouplingSystemDeflection(_2246.CouplingSystemDeflection):
    '''PartToPartShearCouplingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2122.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6158.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6158.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3293.PartToPartShearCouplingPowerFlow':
        '''PartToPartShearCouplingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3293.PartToPartShearCouplingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
