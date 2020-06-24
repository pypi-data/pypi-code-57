'''_282.py

DrawStyleBase
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DRAW_STYLE_BASE = python_net_import('SMT.MastaAPI.Geometry', 'DrawStyleBase')


__docformat__ = 'restructuredtext en'
__all__ = ('DrawStyleBase',)


class DrawStyleBase(_1.APIBase):
    '''DrawStyleBase

    This is a mastapy class.
    '''

    TYPE = _DRAW_STYLE_BASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DrawStyleBase.TYPE'):
        super().__init__(instance_to_wrap)
