'''_1074.py

Number
'''


from mastapy.utility.units_and_measurements import _1038
from mastapy._internal.python_net import python_net_import

_NUMBER = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Number')


__docformat__ = 'restructuredtext en'
__all__ = ('Number',)


class Number(_1038.MeasurementBase):
    '''Number

    This is a mastapy class.
    '''

    TYPE = _NUMBER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Number.TYPE'):
        super().__init__(instance_to_wrap)
