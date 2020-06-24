'''_642.py

CalculationError
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CALCULATION_ERROR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'CalculationError')


__docformat__ = 'restructuredtext en'
__all__ = ('CalculationError',)


class CalculationError(_1.APIBase):
    '''CalculationError

    This is a mastapy class.
    '''

    TYPE = _CALCULATION_ERROR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CalculationError.TYPE'):
        super().__init__(instance_to_wrap)
