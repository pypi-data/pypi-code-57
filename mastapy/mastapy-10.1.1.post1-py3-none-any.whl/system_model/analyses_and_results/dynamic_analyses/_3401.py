'''_3401.py

TorqueConverterTurbineDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2046
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2268
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3386
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'TorqueConverterTurbineDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineDynamicAnalysis',)


class TorqueConverterTurbineDynamicAnalysis(_3386.CouplingHalfDynamicAnalysis):
    '''TorqueConverterTurbineDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2046.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2046.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2268.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2268.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
