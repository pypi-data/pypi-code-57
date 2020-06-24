'''_4283.py

MeasurementComponentModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2005
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6149
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4328
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'MeasurementComponentModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentModalAnalysisAtAStiffness',)


class MeasurementComponentModalAnalysisAtAStiffness(_4328.VirtualComponentModalAnalysisAtAStiffness):
    '''MeasurementComponentModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6149.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6149.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
