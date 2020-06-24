'''_222.py

AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ABSTRACT_STRESS_CYCLES_DATA_FOR_AN_SN_CURVE_OF_A_PLASTIC_MATERIAL = python_net_import('SMT.MastaAPI.Materials', 'AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial',)


class AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial(_1.APIBase):
    '''AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_STRESS_CYCLES_DATA_FOR_AN_SN_CURVE_OF_A_PLASTIC_MATERIAL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_load_cycles(self) -> 'float':
        '''float: 'NumberOfLoadCycles' is the original name of this property.'''

        return self.wrapped.NumberOfLoadCycles

    @number_of_load_cycles.setter
    def number_of_load_cycles(self, value: 'float'):
        self.wrapped.NumberOfLoadCycles = float(value) if value else 0.0
