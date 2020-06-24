'''_4252.py

CVTPulleyModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2121
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4296
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'CVTPulleyModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyModalAnalysisAtAStiffness',)


class CVTPulleyModalAnalysisAtAStiffness(_4296.PulleyModalAnalysisAtAStiffness):
    '''CVTPulleyModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2121.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2121.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
