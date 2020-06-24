'''_3859.py

ClutchModalAnalysis
'''


from mastapy.system_model.part_model.couplings import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2173
from mastapy.system_model.analyses_and_results.system_deflections import _2156
from mastapy.system_model.analyses_and_results.modal_analyses import _3863
from mastapy._internal.python_net import python_net_import

_CLUTCH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ClutchModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchModalAnalysis',)


class ClutchModalAnalysis(_3863.CouplingModalAnalysis):
    '''ClutchModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1988.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2173.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2156.ClutchSystemDeflection':
        '''ClutchSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2156.ClutchSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
