'''_3766.py

CylindricalPlanetGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2066
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3764
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'CylindricalPlanetGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearModalAnalysesAtStiffnesses',)


class CylindricalPlanetGearModalAnalysesAtStiffnesses(_3764.CylindricalGearModalAnalysesAtStiffnesses):
    '''CylindricalPlanetGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2066.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
