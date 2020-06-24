'''_5512.py

SynchroniserModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _1976
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2198
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5496
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'SynchroniserModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserModalAnalysisAtAStiffness',)


class SynchroniserModalAnalysisAtAStiffness(_5496.SpecialisedAssemblyModalAnalysisAtAStiffness):
    '''SynchroniserModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1976.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2198.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
