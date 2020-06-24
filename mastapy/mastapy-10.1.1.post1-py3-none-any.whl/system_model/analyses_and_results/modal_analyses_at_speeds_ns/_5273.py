'''_5273.py

SynchroniserHalfModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2024
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2200
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5275
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'SynchroniserHalfModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfModalAnalysesAtSpeeds',)


class SynchroniserHalfModalAnalysesAtSpeeds(_5275.SynchroniserPartModalAnalysesAtSpeeds):
    '''SynchroniserHalfModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfModalAnalysesAtSpeeds.TYPE'):
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
