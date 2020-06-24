'''_1059.py

CylindricalAccuracyGrader
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1061, _1057, _1065
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_ACCURACY_GRADER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'CylindricalAccuracyGrader')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalAccuracyGrader',)


class CylindricalAccuracyGrader(_1.APIBase):
    '''CylindricalAccuracyGrader

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_ACCURACY_GRADER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalAccuracyGrader.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def single_pitch_deviation(self) -> 'float':
        '''float: 'SinglePitchDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SinglePitchDeviation

    @property
    def total_radial_composite_deviation(self) -> 'float':
        '''float: 'TotalRadialCompositeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalRadialCompositeDeviation

    @property
    def toothto_tooth_radial_composite_deviation(self) -> 'float':
        '''float: 'ToothtoToothRadialCompositeDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothtoToothRadialCompositeDeviation

    @property
    def runout(self) -> 'float':
        '''float: 'Runout' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Runout

    @property
    def tolerance_standard(self) -> 'str':
        '''str: 'ToleranceStandard' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToleranceStandard

    @property
    def accuracy_grades(self) -> '_1061.CylindricalAccuracyGrades':
        '''CylindricalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1061.CylindricalAccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_agma20151_accuracy_grades(self) -> '_1057.AGMA20151AccuracyGrades':
        '''AGMA20151AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AccuracyGrades.__class__.__qualname__ != 'AGMA20151AccuracyGrades':
            raise CastException('Failed to cast accuracy_grades to AGMA20151AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_1057.AGMA20151AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None

    @property
    def accuracy_grades_of_type_iso1328_accuracy_grades(self) -> '_1065.ISO1328AccuracyGrades':
        '''ISO1328AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AccuracyGrades.__class__.__qualname__ != 'ISO1328AccuracyGrades':
            raise CastException('Failed to cast accuracy_grades to ISO1328AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new(_1065.ISO1328AccuracyGrades)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades else None
