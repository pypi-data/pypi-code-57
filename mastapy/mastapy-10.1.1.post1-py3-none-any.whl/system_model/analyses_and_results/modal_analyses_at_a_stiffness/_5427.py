'''_5427.py

ClutchHalfModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2015
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2174
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5443
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ClutchHalfModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfModalAnalysisAtAStiffness',)


class ClutchHalfModalAnalysisAtAStiffness(_5443.CouplingHalfModalAnalysisAtAStiffness):
    '''ClutchHalfModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2015.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2174.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
