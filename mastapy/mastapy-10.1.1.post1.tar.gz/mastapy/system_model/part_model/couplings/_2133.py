'''_2133.py

SpringDamper
'''


from mastapy.system_model.connections_and_sockets.couplings import _1902
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2118
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamper',)


class SpringDamper(_2118.Coupling):
    '''SpringDamper

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamper.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection(self) -> '_1902.SpringDamperConnection':
        '''SpringDamperConnection: 'Connection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1902.SpringDamperConnection)(self.wrapped.Connection) if self.wrapped.Connection else None
