'''_652.py

PlungeShaverSettings
'''


from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _645
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverSettings',)


class PlungeShaverSettings(_1.APIBase):
    '''PlungeShaverSettings

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_solver_initial_guesses(self) -> 'int':
        '''int: 'NumberOfSolverInitialGuesses' is the original name of this property.'''

        return self.wrapped.NumberOfSolverInitialGuesses

    @number_of_solver_initial_guesses.setter
    def number_of_solver_initial_guesses(self, value: 'int'):
        self.wrapped.NumberOfSolverInitialGuesses = int(value) if value else 0

    @property
    def extend_gear_surface_factor(self) -> 'float':
        '''float: 'ExtendGearSurfaceFactor' is the original name of this property.'''

        return self.wrapped.ExtendGearSurfaceFactor

    @extend_gear_surface_factor.setter
    def extend_gear_surface_factor(self, value: 'float'):
        self.wrapped.ExtendGearSurfaceFactor = float(value) if value else 0.0

    @property
    def number_of_gear_tip_transverse_planes(self) -> 'int':
        '''int: 'NumberOfGearTipTransversePlanes' is the original name of this property.'''

        return self.wrapped.NumberOfGearTipTransversePlanes

    @number_of_gear_tip_transverse_planes.setter
    def number_of_gear_tip_transverse_planes(self, value: 'int'):
        self.wrapped.NumberOfGearTipTransversePlanes = int(value) if value else 0

    @property
    def number_of_cutter_transverse_planes(self) -> 'int':
        '''int: 'NumberOfCutterTransversePlanes' is the original name of this property.'''

        return self.wrapped.NumberOfCutterTransversePlanes

    @number_of_cutter_transverse_planes.setter
    def number_of_cutter_transverse_planes(self, value: 'int'):
        self.wrapped.NumberOfCutterTransversePlanes = int(value) if value else 0

    @property
    def number_of_points_on_each_shaver_transverse_plane(self) -> 'int':
        '''int: 'NumberOfPointsOnEachShaverTransversePlane' is the original name of this property.'''

        return self.wrapped.NumberOfPointsOnEachShaverTransversePlane

    @number_of_points_on_each_shaver_transverse_plane.setter
    def number_of_points_on_each_shaver_transverse_plane(self, value: 'int'):
        self.wrapped.NumberOfPointsOnEachShaverTransversePlane = int(value) if value else 0

    @property
    def number_of_points_on_the_tip(self) -> 'int':
        '''int: 'NumberOfPointsOnTheTip' is the original name of this property.'''

        return self.wrapped.NumberOfPointsOnTheTip

    @number_of_points_on_the_tip.setter
    def number_of_points_on_the_tip(self, value: 'int'):
        self.wrapped.NumberOfPointsOnTheTip = int(value) if value else 0

    @property
    def number_of_points_on_the_input_gear_involute(self) -> 'int':
        '''int: 'NumberOfPointsOnTheInputGearInvolute' is the original name of this property.'''

        return self.wrapped.NumberOfPointsOnTheInputGearInvolute

    @number_of_points_on_the_input_gear_involute.setter
    def number_of_points_on_the_input_gear_involute(self, value: 'int'):
        self.wrapped.NumberOfPointsOnTheInputGearInvolute = int(value) if value else 0

    @property
    def lead_display_method(self) -> '_645.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'LeadDisplayMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.LeadDisplayMethod)
        return constructor.new(_645.MicroGeometryDefinitionMethod)(value) if value else None

    @lead_display_method.setter
    def lead_display_method(self, value: '_645.MicroGeometryDefinitionMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LeadDisplayMethod = value

    @property
    def profile_display_method(self) -> '_645.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'ProfileDisplayMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileDisplayMethod)
        return constructor.new(_645.MicroGeometryDefinitionMethod)(value) if value else None

    @profile_display_method.setter
    def profile_display_method(self, value: '_645.MicroGeometryDefinitionMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileDisplayMethod = value
