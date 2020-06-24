'''_661.py

CalculatePitchDeviationAccuracy
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _679
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CALCULATE_PITCH_DEVIATION_ACCURACY = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'CalculatePitchDeviationAccuracy')


__docformat__ = 'restructuredtext en'
__all__ = ('CalculatePitchDeviationAccuracy',)


class CalculatePitchDeviationAccuracy(_1.APIBase):
    '''CalculatePitchDeviationAccuracy

    This is a mastapy class.
    '''

    TYPE = _CALCULATE_PITCH_DEVIATION_ACCURACY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CalculatePitchDeviationAccuracy.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flank_name(self) -> 'str':
        '''str: 'FlankName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FlankName

    @property
    def pitch_deviation_iso132811995e_quality_grade_designed(self) -> 'float':
        '''float: 'PitchDeviationISO132811995EQualityGradeDesigned' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchDeviationISO132811995EQualityGradeDesigned

    @property
    def pitch_deviation_ansiagma20151a01_quality_grade_designed(self) -> 'float':
        '''float: 'PitchDeviationANSIAGMA20151A01QualityGradeDesigned' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchDeviationANSIAGMA20151A01QualityGradeDesigned

    @property
    def single_pitch_deviation(self) -> 'float':
        '''float: 'SinglePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SinglePitchDeviation

    @property
    def cumulative_pitch_deviation(self) -> 'float':
        '''float: 'CumulativePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CumulativePitchDeviation

    @property
    def total_cumulative_pitch_deviation(self) -> 'float':
        '''float: 'TotalCumulativePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalCumulativePitchDeviation

    @property
    def total_cumulative_pitch_deviation_iso132811995e_quality_grade_obtained(self) -> 'float':
        '''float: 'TotalCumulativePitchDeviationISO132811995EQualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalCumulativePitchDeviationISO132811995EQualityGradeObtained

    @property
    def cumulative_pitch_deviation_ansiagma20151a01_quality_grade_obtained(self) -> 'float':
        '''float: 'CumulativePitchDeviationANSIAGMA20151A01QualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CumulativePitchDeviationANSIAGMA20151A01QualityGradeObtained

    @property
    def cumulative_pitch_deviation_iso132811995e_quality_grade_obtained(self) -> 'float':
        '''float: 'CumulativePitchDeviationISO132811995EQualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CumulativePitchDeviationISO132811995EQualityGradeObtained

    @property
    def single_pitch_deviation_iso132811995e_quality_grade_obtained(self) -> 'float':
        '''float: 'SinglePitchDeviationISO132811995EQualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SinglePitchDeviationISO132811995EQualityGradeObtained

    @property
    def single_pitch_deviation_ansiagma20151a01_quality_grade_obtained(self) -> 'float':
        '''float: 'SinglePitchDeviationANSIAGMA20151A01QualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SinglePitchDeviationANSIAGMA20151A01QualityGradeObtained

    @property
    def achieved_pitch_iso132811995e_quality_grade(self) -> 'float':
        '''float: 'AchievedPitchISO132811995EQualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedPitchISO132811995EQualityGrade

    @property
    def achieved_pitch_ansiagma20151a01_quality_grade(self) -> 'float':
        '''float: 'AchievedPitchANSIAGMA20151A01QualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedPitchANSIAGMA20151A01QualityGrade

    @property
    def manufactured_iso132811995e_quality_grades(self) -> 'List[_679.ManufacturedQualityGrade]':
        '''List[ManufacturedQualityGrade]: 'ManufacturedISO132811995EQualityGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ManufacturedISO132811995EQualityGrades, constructor.new(_679.ManufacturedQualityGrade))
        return value

    @property
    def manufactured_ansiagma20151a01_quality_grades(self) -> 'List[_679.ManufacturedQualityGrade]':
        '''List[ManufacturedQualityGrade]: 'ManufacturedANSIAGMA20151A01QualityGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ManufacturedANSIAGMA20151A01QualityGrades, constructor.new(_679.ManufacturedQualityGrade))
        return value
