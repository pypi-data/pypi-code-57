'''_2050.py

PlanetCarrierCreationOptions
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'PlanetCarrierCreationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCreationOptions',)


class PlanetCarrierCreationOptions(_1.APIBase):
    '''PlanetCarrierCreationOptions

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_CREATION_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCreationOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_planets(self) -> 'int':
        '''int: 'NumberOfPlanets' is the original name of this property.'''

        return self.wrapped.NumberOfPlanets

    @number_of_planets.setter
    def number_of_planets(self, value: 'int'):
        self.wrapped.NumberOfPlanets = int(value) if value else 0

    @property
    def diameter(self) -> 'float':
        '''float: 'Diameter' is the original name of this property.'''

        return self.wrapped.Diameter

    @diameter.setter
    def diameter(self, value: 'float'):
        self.wrapped.Diameter = float(value) if value else 0.0
