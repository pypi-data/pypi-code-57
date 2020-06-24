'''_647.py

PlungeShaverCalculation
'''


from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _648, _657
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverCalculation',)


class PlungeShaverCalculation(_1.APIBase):
    '''PlungeShaverCalculation

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_CALCULATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverCalculation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def inputs(self) -> '_648.PlungeShaverCalculationInputs':
        '''PlungeShaverCalculationInputs: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_648.PlungeShaverCalculationInputs)(self.wrapped.Inputs) if self.wrapped.Inputs else None

    @property
    def simulation_of_ideal_shaver_conjugate_to_the_designed_gear(self) -> '_657.VirtualPlungeShaverOutputs':
        '''VirtualPlungeShaverOutputs: 'SimulationOfIdealShaverConjugateToTheDesignedGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_657.VirtualPlungeShaverOutputs)(self.wrapped.SimulationOfIdealShaverConjugateToTheDesignedGear) if self.wrapped.SimulationOfIdealShaverConjugateToTheDesignedGear else None
