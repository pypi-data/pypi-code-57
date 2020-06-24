'''_4501.py

DatumModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1993
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6099
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4479
from mastapy._internal.python_net import python_net_import

_DATUM_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'DatumModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumModalAnalysisAtASpeed',)


class DatumModalAnalysisAtASpeed(_4479.ComponentModalAnalysisAtASpeed):
    '''DatumModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _DATUM_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1993.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6099.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6099.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
