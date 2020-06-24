'''_5347.py

PartToPartShearCouplingConnectionGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1900
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6156
from mastapy.system_model.analyses_and_results.system_deflections import _2293
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5289
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'PartToPartShearCouplingConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionGearWhineAnalysis',)


class PartToPartShearCouplingConnectionGearWhineAnalysis(_5289.CouplingConnectionGearWhineAnalysis):
    '''PartToPartShearCouplingConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1900.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1900.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6156.PartToPartShearCouplingConnectionLoadCase':
        '''PartToPartShearCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6156.PartToPartShearCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2293.PartToPartShearCouplingConnectionSystemDeflection':
        '''PartToPartShearCouplingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2293.PartToPartShearCouplingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
