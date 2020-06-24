'''_3759.py

TorqueConverterPumpGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2021
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2208
from mastapy.system_model.analyses_and_results.system_deflections import _2207
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3745
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'TorqueConverterPumpGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpGearWhineAnalysis',)


class TorqueConverterPumpGearWhineAnalysis(_3745.CouplingHalfGearWhineAnalysis):
    '''TorqueConverterPumpGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2021.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2021.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2208.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2208.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2207.TorqueConverterPumpSystemDeflection':
        '''TorqueConverterPumpSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2207.TorqueConverterPumpSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
