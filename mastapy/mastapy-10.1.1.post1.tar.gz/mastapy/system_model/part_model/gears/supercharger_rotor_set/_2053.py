'''_2053.py

SuperchargerMap
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SUPERCHARGER_MAP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'SuperchargerMap')


__docformat__ = 'restructuredtext en'
__all__ = ('SuperchargerMap',)


class SuperchargerMap(_1.APIBase):
    '''SuperchargerMap

    This is a mastapy class.
    '''

    TYPE = _SUPERCHARGER_MAP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SuperchargerMap.TYPE'):
        super().__init__(instance_to_wrap)
