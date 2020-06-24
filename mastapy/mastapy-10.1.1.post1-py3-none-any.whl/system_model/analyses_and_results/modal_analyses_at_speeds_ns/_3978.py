'''_3978.py

BevelDifferentialPlanetGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2056
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3976
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'BevelDifferentialPlanetGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearModalAnalysesAtSpeeds',)


class BevelDifferentialPlanetGearModalAnalysesAtSpeeds(_3976.BevelDifferentialGearModalAnalysesAtSpeeds):
    '''BevelDifferentialPlanetGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2056.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
