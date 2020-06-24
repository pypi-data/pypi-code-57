'''_1698.py

RollerRibDetail
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ROLLER_RIB_DETAIL = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'RollerRibDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerRibDetail',)


class RollerRibDetail(_1.APIBase):
    '''RollerRibDetail

    This is a mastapy class.
    '''

    TYPE = _ROLLER_RIB_DETAIL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollerRibDetail.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Diameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Diameter) if self.wrapped.Diameter else None

    @diameter.setter
    def diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Diameter = value

    @property
    def present(self) -> 'bool':
        '''bool: 'Present' is the original name of this property.'''

        return self.wrapped.Present

    @present.setter
    def present(self, value: 'bool'):
        self.wrapped.Present = bool(value) if value else False

    @property
    def chamfer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Chamfer' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Chamfer) if self.wrapped.Chamfer else None

    @chamfer.setter
    def chamfer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Chamfer = value

    @property
    def layback_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LaybackAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LaybackAngle) if self.wrapped.LaybackAngle else None

    @layback_angle.setter
    def layback_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LaybackAngle = value

    @property
    def nominal_contact_height_above_race(self) -> 'float':
        '''float: 'NominalContactHeightAboveRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NominalContactHeightAboveRace

    @property
    def height_above_race(self) -> 'float':
        '''float: 'HeightAboveRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HeightAboveRace

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
