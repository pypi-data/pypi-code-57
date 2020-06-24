'''_4787.py

PowerLoadModalAnalysis
'''


from mastapy.system_model.part_model import _2013
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6166
from mastapy.system_model.analyses_and_results.system_deflections import _2299
from mastapy.system_model.analyses_and_results.modal_analyses import _4821
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PowerLoadModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadModalAnalysis',)


class PowerLoadModalAnalysis(_4821.VirtualComponentModalAnalysis):
    '''PowerLoadModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2013.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6166.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6166.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2299.PowerLoadSystemDeflection':
        '''PowerLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2299.PowerLoadSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
