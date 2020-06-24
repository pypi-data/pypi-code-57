'''_487.py

ISOScuffingResultsRow
'''


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical import _493
from mastapy._internal.python_net import python_net_import

_ISO_SCUFFING_RESULTS_ROW = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'ISOScuffingResultsRow')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOScuffingResultsRow',)


class ISOScuffingResultsRow(_493.ScuffingResultsRow):
    '''ISOScuffingResultsRow

    This is a mastapy class.
    '''

    TYPE = _ISO_SCUFFING_RESULTS_ROW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISOScuffingResultsRow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flash_temperature(self) -> 'float':
        '''float: 'FlashTemperature' is the original name of this property.'''

        return self.wrapped.FlashTemperature

    @flash_temperature.setter
    def flash_temperature(self, value: 'float'):
        self.wrapped.FlashTemperature = float(value) if value else 0.0

    @property
    def contact_temperature(self) -> 'float':
        '''float: 'ContactTemperature' is the original name of this property.'''

        return self.wrapped.ContactTemperature

    @contact_temperature.setter
    def contact_temperature(self, value: 'float'):
        self.wrapped.ContactTemperature = float(value) if value else 0.0

    @property
    def approach_factor(self) -> 'float':
        '''float: 'ApproachFactor' is the original name of this property.'''

        return self.wrapped.ApproachFactor

    @approach_factor.setter
    def approach_factor(self, value: 'float'):
        self.wrapped.ApproachFactor = float(value) if value else 0.0

    @property
    def thermo_elastic_factor(self) -> 'float':
        '''float: 'ThermoElasticFactor' is the original name of this property.'''

        return self.wrapped.ThermoElasticFactor

    @thermo_elastic_factor.setter
    def thermo_elastic_factor(self, value: 'float'):
        self.wrapped.ThermoElasticFactor = float(value) if value else 0.0

    @property
    def geometry_factor(self) -> 'float':
        '''float: 'GeometryFactor' is the original name of this property.'''

        return self.wrapped.GeometryFactor

    @geometry_factor.setter
    def geometry_factor(self, value: 'float'):
        self.wrapped.GeometryFactor = float(value) if value else 0.0
