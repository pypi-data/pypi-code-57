'''_2012.py

PointLoad
'''


from mastapy.math_utility.measured_vectors import _1117
from mastapy._internal import constructor
from mastapy.system_model.part_model import _2019
from mastapy._internal.python_net import python_net_import

_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoad',)


class PointLoad(_2019.VirtualComponent):
    '''PointLoad

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoad.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def offset(self) -> '_1117.Vector2DPolar':
        '''Vector2DPolar: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1117.Vector2DPolar)(self.wrapped.Offset) if self.wrapped.Offset else None
