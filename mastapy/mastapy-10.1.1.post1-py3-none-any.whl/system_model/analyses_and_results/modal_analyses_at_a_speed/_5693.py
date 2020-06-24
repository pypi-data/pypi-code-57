'''_5693.py

FaceGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _1997
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2310
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5697
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'FaceGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearModalAnalysisAtASpeed',)


class FaceGearModalAnalysisAtASpeed(_5697.GearModalAnalysisAtASpeed):
    '''FaceGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2310.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2310.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
