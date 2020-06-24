'''_639.py

CutterProcessSimulation
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CUTTER_PROCESS_SIMULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.ProcessSimulation', 'CutterProcessSimulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterProcessSimulation',)


class CutterProcessSimulation(_1.APIBase):
    '''CutterProcessSimulation

    This is a mastapy class.
    '''

    TYPE = _CUTTER_PROCESS_SIMULATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CutterProcessSimulation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_teeth_to_calculate(self) -> 'int':
        '''int: 'NumberOfTeethToCalculate' is the original name of this property.'''

        return self.wrapped.NumberOfTeethToCalculate

    @number_of_teeth_to_calculate.setter
    def number_of_teeth_to_calculate(self, value: 'int'):
        self.wrapped.NumberOfTeethToCalculate = int(value) if value else 0

    @property
    def start_of_measured_lead(self) -> 'float':
        '''float: 'StartOfMeasuredLead' is the original name of this property.'''

        return self.wrapped.StartOfMeasuredLead

    @start_of_measured_lead.setter
    def start_of_measured_lead(self, value: 'float'):
        self.wrapped.StartOfMeasuredLead = float(value) if value else 0.0

    @property
    def end_of_measured_lead(self) -> 'float':
        '''float: 'EndOfMeasuredLead' is the original name of this property.'''

        return self.wrapped.EndOfMeasuredLead

    @end_of_measured_lead.setter
    def end_of_measured_lead(self, value: 'float'):
        self.wrapped.EndOfMeasuredLead = float(value) if value else 0.0

    @property
    def start_of_measured_profile(self) -> 'float':
        '''float: 'StartOfMeasuredProfile' is the original name of this property.'''

        return self.wrapped.StartOfMeasuredProfile

    @start_of_measured_profile.setter
    def start_of_measured_profile(self, value: 'float'):
        self.wrapped.StartOfMeasuredProfile = float(value) if value else 0.0

    @property
    def end_of_measured_profile(self) -> 'float':
        '''float: 'EndOfMeasuredProfile' is the original name of this property.'''

        return self.wrapped.EndOfMeasuredProfile

    @end_of_measured_profile.setter
    def end_of_measured_profile(self, value: 'float'):
        self.wrapped.EndOfMeasuredProfile = float(value) if value else 0.0

    @property
    def rolling_distance_per_step(self) -> 'float':
        '''float: 'RollingDistancePerStep' is the original name of this property.'''

        return self.wrapped.RollingDistancePerStep

    @rolling_distance_per_step.setter
    def rolling_distance_per_step(self, value: 'float'):
        self.wrapped.RollingDistancePerStep = float(value) if value else 0.0

    @property
    def lead_distance_per_step(self) -> 'float':
        '''float: 'LeadDistancePerStep' is the original name of this property.'''

        return self.wrapped.LeadDistancePerStep

    @lead_distance_per_step.setter
    def lead_distance_per_step(self, value: 'float'):
        self.wrapped.LeadDistancePerStep = float(value) if value else 0.0
