'''_1152.py

MeasurementSystem
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MEASUREMENT_SYSTEM = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'MeasurementSystem')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementSystem',)


class MeasurementSystem(Enum):
    '''MeasurementSystem

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _MEASUREMENT_SYSTEM

    __hash__ = None

    METRIC = 0
    IMPERIAL = 1
