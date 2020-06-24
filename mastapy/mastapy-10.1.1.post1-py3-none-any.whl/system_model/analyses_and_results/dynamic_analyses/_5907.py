'''_5907.py

TorqueConverterDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2140
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6200
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5831
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'TorqueConverterDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterDynamicAnalysis',)


class TorqueConverterDynamicAnalysis(_5831.CouplingDynamicAnalysis):
    '''TorqueConverterDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2140.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6200.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6200.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
