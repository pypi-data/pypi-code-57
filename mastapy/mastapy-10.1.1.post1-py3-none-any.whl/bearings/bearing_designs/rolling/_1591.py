'''_1591.py

AsymmetricSphericalRollerBearing
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1695
from mastapy._internal.python_net import python_net_import

_ASYMMETRIC_SPHERICAL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'AsymmetricSphericalRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('AsymmetricSphericalRollerBearing',)


class AsymmetricSphericalRollerBearing(_1695.RollerBearing):
    '''AsymmetricSphericalRollerBearing

    This is a mastapy class.
    '''

    TYPE = _ASYMMETRIC_SPHERICAL_ROLLER_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AsymmetricSphericalRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def major_diameter_offset_from_roller_centre(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MajorDiameterOffsetFromRollerCentre' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MajorDiameterOffsetFromRollerCentre) if self.wrapped.MajorDiameterOffsetFromRollerCentre else None

    @major_diameter_offset_from_roller_centre.setter
    def major_diameter_offset_from_roller_centre(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MajorDiameterOffsetFromRollerCentre = value

    @property
    def element_top_face_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementTopFaceDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementTopFaceDiameter) if self.wrapped.ElementTopFaceDiameter else None

    @element_top_face_diameter.setter
    def element_top_face_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementTopFaceDiameter = value

    @property
    def element_bottom_face_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementBottomFaceDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementBottomFaceDiameter) if self.wrapped.ElementBottomFaceDiameter else None

    @element_bottom_face_diameter.setter
    def element_bottom_face_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementBottomFaceDiameter = value

    @property
    def element_profile_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementProfileRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementProfileRadius) if self.wrapped.ElementProfileRadius else None

    @element_profile_radius.setter
    def element_profile_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementProfileRadius = value

    @property
    def outer_race_groove_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterRaceGrooveRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterRaceGrooveRadius) if self.wrapped.OuterRaceGrooveRadius else None

    @outer_race_groove_radius.setter
    def outer_race_groove_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OuterRaceGrooveRadius = value

    @property
    def inner_race_groove_radius(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerRaceGrooveRadius' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerRaceGrooveRadius) if self.wrapped.InnerRaceGrooveRadius else None

    @inner_race_groove_radius.setter
    def inner_race_groove_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InnerRaceGrooveRadius = value

    @property
    def inner_rib_chamfer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerRibChamfer' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerRibChamfer) if self.wrapped.InnerRibChamfer else None

    @inner_rib_chamfer.setter
    def inner_rib_chamfer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InnerRibChamfer = value

    @property
    def inner_rib_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerRibDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerRibDiameter) if self.wrapped.InnerRibDiameter else None

    @inner_rib_diameter.setter
    def inner_rib_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InnerRibDiameter = value
