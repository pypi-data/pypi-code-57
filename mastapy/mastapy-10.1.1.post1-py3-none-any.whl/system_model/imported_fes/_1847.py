'''_1847.py

DegreeOfFreedomBoundaryCondition
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DEGREE_OF_FREEDOM_BOUNDARY_CONDITION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'DegreeOfFreedomBoundaryCondition')


__docformat__ = 'restructuredtext en'
__all__ = ('DegreeOfFreedomBoundaryCondition',)


class DegreeOfFreedomBoundaryCondition(_1.APIBase):
    '''DegreeOfFreedomBoundaryCondition

    This is a mastapy class.
    '''

    TYPE = _DEGREE_OF_FREEDOM_BOUNDARY_CONDITION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DegreeOfFreedomBoundaryCondition.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def phase(self) -> 'float':
        '''float: 'Phase' is the original name of this property.'''

        return self.wrapped.Phase

    @phase.setter
    def phase(self, value: 'float'):
        self.wrapped.Phase = float(value) if value else 0.0
