'''_790.py

ShavingDynamicsConfiguration
'''


from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _787, _772, _776
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_CONFIGURATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsConfiguration',)


class ShavingDynamicsConfiguration(_1.APIBase):
    '''ShavingDynamicsConfiguration

    This is a mastapy class.
    '''

    TYPE = _SHAVING_DYNAMICS_CONFIGURATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamicsConfiguration.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conventional_shaving_dynamics(self) -> '_787.ShavingDynamicsCalculation[_772.ConventionalShavingDynamics]':
        '''ShavingDynamicsCalculation[ConventionalShavingDynamics]: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_787.ShavingDynamicsCalculation)[_772.ConventionalShavingDynamics](self.wrapped.ConventionalShavingDynamics) if self.wrapped.ConventionalShavingDynamics else None

    @property
    def plunge_shaving_dynamics(self) -> '_787.ShavingDynamicsCalculation[_776.PlungeShaverDynamics]':
        '''ShavingDynamicsCalculation[PlungeShaverDynamics]: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_787.ShavingDynamicsCalculation)[_776.PlungeShaverDynamics](self.wrapped.PlungeShavingDynamics) if self.wrapped.PlungeShavingDynamics else None
