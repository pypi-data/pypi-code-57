'''_864.py

GearStiffness
'''


from mastapy.nodal_analysis import _91
from mastapy._internal.python_net import python_net_import

_GEAR_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('GearStiffness',)


class GearStiffness(_91.FEStiffness):
    '''GearStiffness

    This is a mastapy class.
    '''

    TYPE = _GEAR_STIFFNESS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearStiffness.TYPE'):
        super().__init__(instance_to_wrap)
