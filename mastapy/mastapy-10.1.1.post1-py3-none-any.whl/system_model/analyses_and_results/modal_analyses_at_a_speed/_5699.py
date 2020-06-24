'''_5699.py

GuideDxfModelModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1921
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2279
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5668
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'GuideDxfModelModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelModalAnalysisAtASpeed',)


class GuideDxfModelModalAnalysisAtASpeed(_5668.ComponentModalAnalysisAtASpeed):
    '''GuideDxfModelModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1921.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1921.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2279.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2279.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
