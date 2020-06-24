'''_4502.py

ExternalCADModelModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1996
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6112
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4479
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ExternalCADModelModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelModalAnalysisAtASpeed',)


class ExternalCADModelModalAnalysisAtASpeed(_4479.ComponentModalAnalysisAtASpeed):
    '''ExternalCADModelModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6112.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6112.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
