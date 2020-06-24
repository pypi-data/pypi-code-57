'''_5502.py

SpringDamperModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _1990
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2194
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5444
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'SpringDamperModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperModalAnalysisAtAStiffness',)


class SpringDamperModalAnalysisAtAStiffness(_5444.CouplingModalAnalysisAtAStiffness):
    '''SpringDamperModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1990.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2194.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
