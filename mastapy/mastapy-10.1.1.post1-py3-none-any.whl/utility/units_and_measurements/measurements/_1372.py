'''_1372.py

Viscosity
'''


from mastapy.utility.units_and_measurements import _1035
from mastapy._internal.python_net import python_net_import

_VISCOSITY = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Viscosity')


__docformat__ = 'restructuredtext en'
__all__ = ('Viscosity',)


class Viscosity(_1035.MeasurementBase):
    '''Viscosity

    This is a mastapy class.
    '''

    TYPE = _VISCOSITY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Viscosity.TYPE'):
        super().__init__(instance_to_wrap)
