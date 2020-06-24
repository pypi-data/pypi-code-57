'''_5348.py

PartToPartShearCouplingGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2122
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6158
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5290
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'PartToPartShearCouplingGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingGearWhineAnalysis',)


class PartToPartShearCouplingGearWhineAnalysis(_5290.CouplingGearWhineAnalysis):
    '''PartToPartShearCouplingGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingGearWhineAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2295.PartToPartShearCouplingSystemDeflection':
        '''PartToPartShearCouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2295.PartToPartShearCouplingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
