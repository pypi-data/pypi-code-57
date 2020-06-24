'''_1939.py

VirtualComponent
'''


from mastapy.system_model.part_model import _1928
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponent',)


class VirtualComponent(_1928.MountableComponent):
    '''VirtualComponent

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponent.TYPE'):
        super().__init__(instance_to_wrap)
