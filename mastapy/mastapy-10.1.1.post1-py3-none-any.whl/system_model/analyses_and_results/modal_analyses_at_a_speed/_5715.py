'''_5715.py

MeasurementComponentModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1927
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2285
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5757
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'MeasurementComponentModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentModalAnalysisAtASpeed',)


class MeasurementComponentModalAnalysisAtASpeed(_5757.VirtualComponentModalAnalysisAtASpeed):
    '''MeasurementComponentModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1927.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1927.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2285.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2285.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
