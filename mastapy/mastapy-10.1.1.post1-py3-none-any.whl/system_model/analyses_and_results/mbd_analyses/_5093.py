'''_5093.py

TorqueConverterPumpMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2141
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6201
from mastapy.system_model.analyses_and_results.mbd_analyses import _5005
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterPumpMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpMultiBodyDynamicsAnalysis',)


class TorqueConverterPumpMultiBodyDynamicsAnalysis(_5005.CouplingHalfMultiBodyDynamicsAnalysis):
    '''TorqueConverterPumpMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2141.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2141.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6201.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6201.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
