'''_695.py

ProcessTotalModificationCalculation
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_TOTAL_MODIFICATION_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessTotalModificationCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessTotalModificationCalculation',)


class ProcessTotalModificationCalculation(_1.APIBase):
    '''ProcessTotalModificationCalculation

    This is a mastapy class.
    '''

    TYPE = _PROCESS_TOTAL_MODIFICATION_CALCULATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessTotalModificationCalculation.TYPE'):
        super().__init__(instance_to_wrap)
