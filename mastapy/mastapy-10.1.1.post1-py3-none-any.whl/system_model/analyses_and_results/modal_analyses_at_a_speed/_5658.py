'''_5658.py

BevelDifferentialSunGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5655
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'BevelDifferentialSunGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearModalAnalysisAtASpeed',)


class BevelDifferentialSunGearModalAnalysisAtASpeed(_5655.BevelDifferentialGearModalAnalysisAtASpeed):
    '''BevelDifferentialSunGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2009.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
