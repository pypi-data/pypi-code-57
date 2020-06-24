'''_4535.py

PlanetaryGearSetModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2081
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4499
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'PlanetaryGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetModalAnalysisAtASpeed',)


class PlanetaryGearSetModalAnalysisAtASpeed(_4499.CylindricalGearSetModalAnalysisAtASpeed):
    '''PlanetaryGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2081.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2081.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
