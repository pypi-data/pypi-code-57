'''_3877.py

TorqueConverterModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _1991
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2206
from mastapy.system_model.analyses_and_results.system_deflections import _2205
from mastapy.system_model.analyses_and_results.modal_analyses import _3863
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'TorqueConverterModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterModalAnalysis',)


class TorqueConverterModalAnalysis(_3863.CouplingModalAnalysis):
    '''TorqueConverterModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1991.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1991.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2206.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2205.TorqueConverterSystemDeflection':
        '''TorqueConverterSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2205.TorqueConverterSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
