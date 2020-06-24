'''_660.py

PointOfInterest
'''


from mastapy.gears.manufacturing.cylindrical import _631
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_POINT_OF_INTEREST = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PointOfInterest')


__docformat__ = 'restructuredtext en'
__all__ = ('PointOfInterest',)


class PointOfInterest(_1.APIBase):
    '''PointOfInterest

    This is a mastapy class.
    '''

    TYPE = _POINT_OF_INTEREST
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointOfInterest.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flank(self) -> '_631.Flank':
        '''Flank: 'Flank' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Flank)
        return constructor.new(_631.Flank)(value) if value else None

    @flank.setter
    def flank(self, value: '_631.Flank'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Flank = value

    @property
    def radius(self) -> 'float':
        '''float: 'Radius' is the original name of this property.'''

        return self.wrapped.Radius

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value else 0.0

    @property
    def face_width(self) -> 'float':
        '''float: 'FaceWidth' is the original name of this property.'''

        return self.wrapped.FaceWidth

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def modification(self) -> 'float':
        '''float: 'Modification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Modification
