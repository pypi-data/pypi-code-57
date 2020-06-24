'''_1537.py

RaceReactionForces
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_RACE_REACTION_FORCES = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'RaceReactionForces')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceReactionForces',)


class RaceReactionForces(_1.APIBase):
    '''RaceReactionForces

    This is a mastapy class.
    '''

    TYPE = _RACE_REACTION_FORCES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceReactionForces.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def x(self) -> 'float':
        '''float: 'X' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.X

    @property
    def y(self) -> 'float':
        '''float: 'Y' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Y

    @property
    def z(self) -> 'float':
        '''float: 'Z' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Z
