'''_54.py

ShaftPointStressCycleReporting
'''


from mastapy._internal import constructor
from mastapy.shafts import _53
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_POINT_STRESS_CYCLE_REPORTING = python_net_import('SMT.MastaAPI.Shafts', 'ShaftPointStressCycleReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftPointStressCycleReporting',)


class ShaftPointStressCycleReporting(_1.APIBase):
    '''ShaftPointStressCycleReporting

    This is a mastapy class.
    '''

    TYPE = _SHAFT_POINT_STRESS_CYCLE_REPORTING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftPointStressCycleReporting.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_cycles(self) -> 'float':
        '''float: 'NumberOfCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCycles

    @property
    def equivalent_alternating_stress(self) -> 'float':
        '''float: 'EquivalentAlternatingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquivalentAlternatingStress

    @property
    def fatigue_strength(self) -> 'float':
        '''float: 'FatigueStrength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FatigueStrength

    @property
    def nominal_stress(self) -> '_53.ShaftPointStressCycle':
        '''ShaftPointStressCycle: 'NominalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_53.ShaftPointStressCycle)(self.wrapped.NominalStress) if self.wrapped.NominalStress else None

    @property
    def stress(self) -> '_53.ShaftPointStressCycle':
        '''ShaftPointStressCycle: 'Stress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_53.ShaftPointStressCycle)(self.wrapped.Stress) if self.wrapped.Stress else None
