'''_685.py

MountingError
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MOUNTING_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'MountingError')


__docformat__ = 'restructuredtext en'
__all__ = ('MountingError',)


class MountingError(_1.APIBase):
    '''MountingError

    This is a mastapy class.
    '''

    TYPE = _MOUNTING_ERROR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountingError.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def first_section_radial_runout(self) -> 'float':
        '''float: 'FirstSectionRadialRunout' is the original name of this property.'''

        return self.wrapped.FirstSectionRadialRunout

    @first_section_radial_runout.setter
    def first_section_radial_runout(self, value: 'float'):
        self.wrapped.FirstSectionRadialRunout = float(value) if value else 0.0

    @property
    def second_section_radial_runout(self) -> 'float':
        '''float: 'SecondSectionRadialRunout' is the original name of this property.'''

        return self.wrapped.SecondSectionRadialRunout

    @second_section_radial_runout.setter
    def second_section_radial_runout(self, value: 'float'):
        self.wrapped.SecondSectionRadialRunout = float(value) if value else 0.0

    @property
    def first_section_phase_angle(self) -> 'float':
        '''float: 'FirstSectionPhaseAngle' is the original name of this property.'''

        return self.wrapped.FirstSectionPhaseAngle

    @first_section_phase_angle.setter
    def first_section_phase_angle(self, value: 'float'):
        self.wrapped.FirstSectionPhaseAngle = float(value) if value else 0.0

    @property
    def second_section_phase_angle(self) -> 'float':
        '''float: 'SecondSectionPhaseAngle' is the original name of this property.'''

        return self.wrapped.SecondSectionPhaseAngle

    @second_section_phase_angle.setter
    def second_section_phase_angle(self, value: 'float'):
        self.wrapped.SecondSectionPhaseAngle = float(value) if value else 0.0

    @property
    def distance_between_two_sections(self) -> 'float':
        '''float: 'DistanceBetweenTwoSections' is the original name of this property.'''

        return self.wrapped.DistanceBetweenTwoSections

    @distance_between_two_sections.setter
    def distance_between_two_sections(self, value: 'float'):
        self.wrapped.DistanceBetweenTwoSections = float(value) if value else 0.0
