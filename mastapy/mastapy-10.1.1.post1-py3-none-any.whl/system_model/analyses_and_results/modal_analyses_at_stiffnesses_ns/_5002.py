'''_5002.py

PlanetaryGearSetModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _1986
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _4968
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'PlanetaryGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetModalAnalysesAtStiffnesses',)


class PlanetaryGearSetModalAnalysesAtStiffnesses(_4968.CylindricalGearSetModalAnalysesAtStiffnesses):
    '''PlanetaryGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1986.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
