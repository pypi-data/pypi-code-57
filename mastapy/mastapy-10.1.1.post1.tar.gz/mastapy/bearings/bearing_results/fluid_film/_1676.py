'''_1676.py

LoadedPlainJournalBearingRow
'''


from mastapy.bearings import _1469
from mastapy._internal import constructor, conversion
from mastapy.scripting import _712
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOADED_PLAIN_JOURNAL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.FluidFilm', 'LoadedPlainJournalBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedPlainJournalBearingRow',)


class LoadedPlainJournalBearingRow(_1.APIBase):
    '''LoadedPlainJournalBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_PLAIN_JOURNAL_BEARING_ROW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedPlainJournalBearingRow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def row(self) -> '_1469.BearingRow':
        '''BearingRow: 'Row' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Row)
        return constructor.new(_1469.BearingRow)(value) if value else None

    @property
    def eccentricity_ratio(self) -> 'float':
        '''float: 'EccentricityRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EccentricityRatio

    @property
    def minimum_film_thickness_at_row_centre(self) -> 'float':
        '''float: 'MinimumFilmThicknessAtRowCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumFilmThicknessAtRowCentre

    @property
    def clipped_minimum_film_thickness_at_row_centre(self) -> 'float':
        '''float: 'ClippedMinimumFilmThicknessAtRowCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClippedMinimumFilmThicknessAtRowCentre

    @property
    def angular_position_of_the_minimum_film_thickness_from_the_x_axis(self) -> 'float':
        '''float: 'AngularPositionOfTheMinimumFilmThicknessFromTheXAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularPositionOfTheMinimumFilmThicknessFromTheXAxis

    @property
    def attitude_force(self) -> 'float':
        '''float: 'AttitudeForce' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AttitudeForce

    @property
    def force_x(self) -> 'float':
        '''float: 'ForceX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceX

    @property
    def force_y(self) -> 'float':
        '''float: 'ForceY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceY

    @property
    def attitude_angle(self) -> 'float':
        '''float: 'AttitudeAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AttitudeAngle

    @property
    def sommerfeld_number(self) -> 'float':
        '''float: 'SommerfeldNumber' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SommerfeldNumber

    @property
    def coefficient_of_traction(self) -> 'float':
        '''float: 'CoefficientOfTraction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientOfTraction

    @property
    def non_dimensional_load(self) -> 'float':
        '''float: 'NonDimensionalLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NonDimensionalLoad

    @property
    def radial_load_per_unit_of_projected_area(self) -> 'float':
        '''float: 'RadialLoadPerUnitOfProjectedArea' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RadialLoadPerUnitOfProjectedArea

    @property
    def journal_bearing_loading_chart(self) -> '_712.SMTBitmap':
        '''SMTBitmap: 'JournalBearingLoadingChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_712.SMTBitmap)(self.wrapped.JournalBearingLoadingChart) if self.wrapped.JournalBearingLoadingChart else None
