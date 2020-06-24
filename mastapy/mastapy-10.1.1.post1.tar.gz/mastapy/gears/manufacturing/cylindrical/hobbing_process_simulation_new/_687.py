'''_687.py

ProcessGearShape
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PROCESS_GEAR_SHAPE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessGearShape')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessGearShape',)


class ProcessGearShape(_1.APIBase):
    '''ProcessGearShape

    This is a mastapy class.
    '''

    TYPE = _PROCESS_GEAR_SHAPE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ProcessGearShape.TYPE'):
        super().__init__(instance_to_wrap)
