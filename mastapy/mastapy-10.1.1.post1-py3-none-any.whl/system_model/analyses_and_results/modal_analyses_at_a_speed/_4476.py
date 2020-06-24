'''_4476.py

ClutchHalfModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2114
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6068
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4492
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ClutchHalfModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfModalAnalysisAtASpeed',)


class ClutchHalfModalAnalysisAtASpeed(_4492.CouplingHalfModalAnalysisAtASpeed):
    '''ClutchHalfModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2114.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6068.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6068.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
