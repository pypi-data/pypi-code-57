'''_4903.py

CentreDistanceExplorer
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CENTRE_DISTANCE_EXPLORER = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CentreDistanceExplorer')


__docformat__ = 'restructuredtext en'
__all__ = ('CentreDistanceExplorer',)


class CentreDistanceExplorer(_1.APIBase):
    '''CentreDistanceExplorer

    This is a mastapy class.
    '''

    TYPE = _CENTRE_DISTANCE_EXPLORER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CentreDistanceExplorer.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def start_factor(self) -> 'float':
        '''float: 'StartFactor' is the original name of this property.'''

        return self.wrapped.StartFactor

    @start_factor.setter
    def start_factor(self, value: 'float'):
        self.wrapped.StartFactor = float(value) if value else 0.0

    @property
    def end_factor(self) -> 'float':
        '''float: 'EndFactor' is the original name of this property.'''

        return self.wrapped.EndFactor

    @end_factor.setter
    def end_factor(self, value: 'float'):
        self.wrapped.EndFactor = float(value) if value else 0.0

    @property
    def number_of_steps(self) -> 'int':
        '''int: 'NumberOfSteps' is the original name of this property.'''

        return self.wrapped.NumberOfSteps

    @number_of_steps.setter
    def number_of_steps(self, value: 'int'):
        self.wrapped.NumberOfSteps = int(value) if value else 0

    @property
    def working_directory(self) -> 'str':
        '''str: 'WorkingDirectory' is the original name of this property.'''

        return self.wrapped.WorkingDirectory

    @working_directory.setter
    def working_directory(self, value: 'str'):
        self.wrapped.WorkingDirectory = str(value) if value else None
