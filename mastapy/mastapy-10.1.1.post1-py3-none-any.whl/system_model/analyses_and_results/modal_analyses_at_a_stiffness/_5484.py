'''_5484.py

PlanetaryGearSetModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _1986
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _5450
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'PlanetaryGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetModalAnalysisAtAStiffness',)


class PlanetaryGearSetModalAnalysisAtAStiffness(_5450.CylindricalGearSetModalAnalysisAtAStiffness):
    '''PlanetaryGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1986.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
