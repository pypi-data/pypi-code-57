'''_2135.py

Synchroniser
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2139, _2137
from mastapy.system_model.connections_and_sockets.couplings import _1894
from mastapy.system_model.part_model import _2017
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')


__docformat__ = 'restructuredtext en'
__all__ = ('Synchroniser',)


class Synchroniser(_2017.SpecialisedAssembly):
    '''Synchroniser

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Synchroniser.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def has_left_cone(self) -> 'bool':
        '''bool: 'HasLeftCone' is the original name of this property.'''

        return self.wrapped.HasLeftCone

    @has_left_cone.setter
    def has_left_cone(self, value: 'bool'):
        self.wrapped.HasLeftCone = bool(value) if value else False

    @property
    def has_right_cone(self) -> 'bool':
        '''bool: 'HasRightCone' is the original name of this property.'''

        return self.wrapped.HasRightCone

    @has_right_cone.setter
    def has_right_cone(self, value: 'bool'):
        self.wrapped.HasRightCone = bool(value) if value else False

    @property
    def hub_and_sleeve(self) -> '_2139.SynchroniserSleeve':
        '''SynchroniserSleeve: 'HubAndSleeve' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.SynchroniserSleeve)(self.wrapped.HubAndSleeve) if self.wrapped.HubAndSleeve else None

    @property
    def left_cone(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'LeftCone' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.LeftCone) if self.wrapped.LeftCone else None

    @property
    def right_cone(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'RightCone' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.RightCone) if self.wrapped.RightCone else None

    @property
    def clutch_connection_left(self) -> '_1894.ClutchConnection':
        '''ClutchConnection: 'ClutchConnectionLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ClutchConnection)(self.wrapped.ClutchConnectionLeft) if self.wrapped.ClutchConnectionLeft else None

    @property
    def clutch_connection_right(self) -> '_1894.ClutchConnection':
        '''ClutchConnection: 'ClutchConnectionRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ClutchConnection)(self.wrapped.ClutchConnectionRight) if self.wrapped.ClutchConnectionRight else None
