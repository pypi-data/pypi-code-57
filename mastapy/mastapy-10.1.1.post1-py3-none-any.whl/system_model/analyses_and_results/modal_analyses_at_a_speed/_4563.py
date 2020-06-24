'''_4563.py

SynchroniserModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2135
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6194
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4547
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'SynchroniserModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserModalAnalysisAtASpeed',)


class SynchroniserModalAnalysisAtASpeed(_4547.SpecialisedAssemblyModalAnalysisAtASpeed):
    '''SynchroniserModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2135.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6194.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6194.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
