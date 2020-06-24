'''_544.py

PlungeShavingDynamicsViewModel
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _540, _554, _539
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVING_DYNAMICS_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'PlungeShavingDynamicsViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShavingDynamicsViewModel',)


class PlungeShavingDynamicsViewModel(_554.ShavingDynamicsViewModel['_539.PlungeShaverDynamics']):
    '''PlungeShavingDynamicsViewModel

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVING_DYNAMICS_VIEW_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShavingDynamicsViewModel.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def transverse_plane_on_gear_for_analysis(self) -> 'float':
        '''float: 'TransversePlaneOnGearForAnalysis' is the original name of this property.'''

        return self.wrapped.TransversePlaneOnGearForAnalysis

    @transverse_plane_on_gear_for_analysis.setter
    def transverse_plane_on_gear_for_analysis(self, value: 'float'):
        self.wrapped.TransversePlaneOnGearForAnalysis = float(value) if value else 0.0

    @property
    def settings(self) -> '_540.PlungeShaverDynamicSettings':
        '''PlungeShaverDynamicSettings: 'Settings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_540.PlungeShaverDynamicSettings)(self.wrapped.Settings) if self.wrapped.Settings else None
