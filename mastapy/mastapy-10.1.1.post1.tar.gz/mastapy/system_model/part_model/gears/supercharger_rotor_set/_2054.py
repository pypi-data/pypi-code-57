'''_2054.py

SuperchargerMaps
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SUPERCHARGER_MAPS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'SuperchargerMaps')


__docformat__ = 'restructuredtext en'
__all__ = ('SuperchargerMaps',)


class SuperchargerMaps(_1.APIBase):
    '''SuperchargerMaps

    This is a mastapy class.
    '''

    TYPE = _SUPERCHARGER_MAPS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SuperchargerMaps.TYPE'):
        super().__init__(instance_to_wrap)
