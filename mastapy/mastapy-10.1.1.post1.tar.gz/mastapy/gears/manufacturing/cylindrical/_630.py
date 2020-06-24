'''_630.py

GearSetConfigViewModel
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SET_CONFIG_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'GearSetConfigViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetConfigViewModel',)


class GearSetConfigViewModel(_1.APIBase):
    '''GearSetConfigViewModel

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_CONFIG_VIEW_MODEL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetConfigViewModel.TYPE'):
        super().__init__(instance_to_wrap)
