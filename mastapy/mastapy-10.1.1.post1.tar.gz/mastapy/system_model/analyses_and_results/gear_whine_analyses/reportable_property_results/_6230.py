'''_6230.py

GearWhineAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.reportable_property_results import _6233, _6228
from mastapy.utility.units_and_measurements.measurements import (
    _1326, _1371, _1280, _1319,
    _1341, _1342
)
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_RESULTS_BROKEN_DOWN_BY_SURFACE_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'GearWhineAnalysisResultsBrokenDownBySurfaceWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisResultsBrokenDownBySurfaceWithinAHarmonic',)


class GearWhineAnalysisResultsBrokenDownBySurfaceWithinAHarmonic(_6228.GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic):
    '''GearWhineAnalysisResultsBrokenDownBySurfaceWithinAHarmonic

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_RESULTS_BROKEN_DOWN_BY_SURFACE_WITHIN_A_HARMONIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisResultsBrokenDownBySurfaceWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def surface_name(self) -> 'str':
        '''str: 'SurfaceName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SurfaceName

    @property
    def root_mean_squared_normal_displacement(self) -> '_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic[_1326.LengthVeryShort, _1371.VelocitySmall]':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic[LengthVeryShort, VelocitySmall]: 'RootMeanSquaredNormalDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)[_1326.LengthVeryShort, _1371.VelocitySmall](self.wrapped.RootMeanSquaredNormalDisplacement) if self.wrapped.RootMeanSquaredNormalDisplacement else None

    @property
    def root_mean_squared_normal_velocity(self) -> '_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic[_1371.VelocitySmall, _1280.Acceleration]':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic[VelocitySmall, Acceleration]: 'RootMeanSquaredNormalVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)[_1371.VelocitySmall, _1280.Acceleration](self.wrapped.RootMeanSquaredNormalVelocity) if self.wrapped.RootMeanSquaredNormalVelocity else None

    @property
    def maximum_normal_velocity(self) -> '_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic[_1371.VelocitySmall, _1280.Acceleration]':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic[VelocitySmall, Acceleration]: 'MaximumNormalVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)[_1371.VelocitySmall, _1280.Acceleration](self.wrapped.MaximumNormalVelocity) if self.wrapped.MaximumNormalVelocity else None

    @property
    def root_mean_squared_normal_acceleration(self) -> '_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic[_1280.Acceleration, _1319.Jerk]':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic[Acceleration, Jerk]: 'RootMeanSquaredNormalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)[_1280.Acceleration, _1319.Jerk](self.wrapped.RootMeanSquaredNormalAcceleration) if self.wrapped.RootMeanSquaredNormalAcceleration else None

    @property
    def airborne_sound_power(self) -> '_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic[_1341.PowerSmall, _1342.PowerSmallPerUnitTime]':
        '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic[PowerSmall, PowerSmallPerUnitTime]: 'AirborneSoundPower' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.ResultsForResponseOfAComponentOrSurfaceInAHarmonic)[_1341.PowerSmall, _1342.PowerSmallPerUnitTime](self.wrapped.AirborneSoundPower) if self.wrapped.AirborneSoundPower else None
