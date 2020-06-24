'''_3874.py

SynchroniserHalfModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _2024
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2200
from mastapy.system_model.analyses_and_results.system_deflections import _2199
from mastapy.system_model.analyses_and_results.modal_analyses import _3875
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'SynchroniserHalfModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfModalAnalysis',)


class SynchroniserHalfModalAnalysis(_3875.SynchroniserPartModalAnalysis):
    '''SynchroniserHalfModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2024.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2200.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2199.SynchroniserHalfSystemDeflection':
        '''SynchroniserHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2199.SynchroniserHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
