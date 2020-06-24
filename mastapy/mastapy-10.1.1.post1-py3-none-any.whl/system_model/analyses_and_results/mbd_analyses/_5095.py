'''_5095.py

TorqueConverterTurbineMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2143
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6202
from mastapy.system_model.analyses_and_results.mbd_analyses import _5005
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterTurbineMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineMultiBodyDynamicsAnalysis',)


class TorqueConverterTurbineMultiBodyDynamicsAnalysis(_5005.CouplingHalfMultiBodyDynamicsAnalysis):
    '''TorqueConverterTurbineMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2143.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2143.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6202.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6202.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
