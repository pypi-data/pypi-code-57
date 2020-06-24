'''_5039.py

UnbalancedMassModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _1938
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2303
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5040
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'UnbalancedMassModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassModalAnalysesAtStiffnesses',)


class UnbalancedMassModalAnalysesAtStiffnesses(_5040.VirtualComponentModalAnalysesAtStiffnesses):
    '''UnbalancedMassModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassModalAnalysesAtStiffnesses.TYPE'):
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
