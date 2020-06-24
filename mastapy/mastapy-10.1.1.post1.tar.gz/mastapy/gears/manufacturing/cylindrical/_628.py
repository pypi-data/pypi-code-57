'''_628.py

GearManufacturingConfigurationViewModel
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_MANUFACTURING_CONFIGURATION_VIEW_MODEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'GearManufacturingConfigurationViewModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearManufacturingConfigurationViewModel',)


class GearManufacturingConfigurationViewModel(_1.APIBase):
    '''GearManufacturingConfigurationViewModel

    This is a mastapy class.
    '''

    TYPE = _GEAR_MANUFACTURING_CONFIGURATION_VIEW_MODEL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearManufacturingConfigurationViewModel.TYPE'):
        super().__init__(instance_to_wrap)
