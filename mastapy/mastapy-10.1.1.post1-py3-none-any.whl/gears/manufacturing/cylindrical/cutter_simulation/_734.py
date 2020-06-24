'''_734.py

HobSimulationCalculator
'''


from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _750
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _735
from mastapy._internal.python_net import python_net_import

_HOB_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'HobSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('HobSimulationCalculator',)


class HobSimulationCalculator(_735.RackSimulationCalculator):
    '''HobSimulationCalculator

    This is a mastapy class.
    '''

    TYPE = _HOB_SIMULATION_CALCULATOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def hob(self) -> '_750.CylindricalGearHobShape':
        '''CylindricalGearHobShape: 'Hob' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_750.CylindricalGearHobShape)(self.wrapped.Hob) if self.wrapped.Hob else None
