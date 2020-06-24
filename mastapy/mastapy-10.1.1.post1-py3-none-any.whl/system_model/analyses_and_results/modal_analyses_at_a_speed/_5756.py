'''_5756.py

UnbalancedMassModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1938
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2303
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5757
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'UnbalancedMassModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassModalAnalysisAtASpeed',)


class UnbalancedMassModalAnalysisAtASpeed(_5757.VirtualComponentModalAnalysisAtASpeed):
    '''UnbalancedMassModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2303.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2303.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
