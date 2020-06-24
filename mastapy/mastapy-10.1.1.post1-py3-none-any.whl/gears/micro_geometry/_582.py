'''_582.py

Modification
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'Modification')


__docformat__ = 'restructuredtext en'
__all__ = ('Modification',)


class Modification(_1.APIBase):
    '''Modification

    This is a mastapy class.
    '''

    TYPE = _MODIFICATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Modification.TYPE'):
        super().__init__(instance_to_wrap)
