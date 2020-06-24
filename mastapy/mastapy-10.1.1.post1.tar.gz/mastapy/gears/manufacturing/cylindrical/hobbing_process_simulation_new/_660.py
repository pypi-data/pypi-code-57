'''_660.py

CalculateLeadDeviationAccuracy
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _679
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CALCULATE_LEAD_DEVIATION_ACCURACY = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'CalculateLeadDeviationAccuracy')


__docformat__ = 'restructuredtext en'
__all__ = ('CalculateLeadDeviationAccuracy',)


class CalculateLeadDeviationAccuracy(_1.APIBase):
    '''CalculateLeadDeviationAccuracy

    This is a mastapy class.
    '''

    TYPE = _CALCULATE_LEAD_DEVIATION_ACCURACY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CalculateLeadDeviationAccuracy.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flank_name(self) -> 'str':
        '''str: 'FlankName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FlankName

    @property
    def total_helix_deviation(self) -> 'float':
        '''float: 'TotalHelixDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalHelixDeviation

    @property
    def helix_form_deviation(self) -> 'float':
        '''float: 'HelixFormDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixFormDeviation

    @property
    def helix_slope_deviation(self) -> 'float':
        '''float: 'HelixSlopeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixSlopeDeviation

    @property
    def total_helix_deviation_iso132811995e_quality_grade_obtained(self) -> 'float':
        '''float: 'TotalHelixDeviationISO132811995EQualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalHelixDeviationISO132811995EQualityGradeObtained

    @property
    def total_helix_deviation_ansiagma20151a01_quality_grade_obtained(self) -> 'float':
        '''float: 'TotalHelixDeviationANSIAGMA20151A01QualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalHelixDeviationANSIAGMA20151A01QualityGradeObtained

    @property
    def helix_form_deviation_iso132811995e_quality_grade_obtained(self) -> 'float':
        '''float: 'HelixFormDeviationISO132811995EQualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixFormDeviationISO132811995EQualityGradeObtained

    @property
    def helix_form_deviation_ansiagma20151a01_quality_grade_obtained(self) -> 'float':
        '''float: 'HelixFormDeviationANSIAGMA20151A01QualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixFormDeviationANSIAGMA20151A01QualityGradeObtained

    @property
    def helix_slope_deviation_iso132811995e_quality_grade_obtained(self) -> 'float':
        '''float: 'HelixSlopeDeviationISO132811995EQualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixSlopeDeviationISO132811995EQualityGradeObtained

    @property
    def helix_slope_deviation_ansiagma20151a01_quality_grade_obtained(self) -> 'float':
        '''float: 'HelixSlopeDeviationANSIAGMA20151A01QualityGradeObtained' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixSlopeDeviationANSIAGMA20151A01QualityGradeObtained

    @property
    def helix_deviation_iso132811995e_quality_grade_designed(self) -> 'float':
        '''float: 'HelixDeviationISO132811995EQualityGradeDesigned' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixDeviationISO132811995EQualityGradeDesigned

    @property
    def helix_deviation_ansiagma20151a01_quality_grade_designed(self) -> 'float':
        '''float: 'HelixDeviationANSIAGMA20151A01QualityGradeDesigned' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HelixDeviationANSIAGMA20151A01QualityGradeDesigned

    @property
    def achieved_lead_iso132811995e_quality_grade(self) -> 'float':
        '''float: 'AchievedLeadISO132811995EQualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedLeadISO132811995EQualityGrade

    @property
    def achieved_lead_ansiagma20151a01_quality_grade(self) -> 'float':
        '''float: 'AchievedLeadANSIAGMA20151A01QualityGrade' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AchievedLeadANSIAGMA20151A01QualityGrade

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
