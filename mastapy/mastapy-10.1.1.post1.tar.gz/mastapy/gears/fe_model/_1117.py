'''_1117.py

GearMeshingElementOptions
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_MESHING_ELEMENT_OPTIONS = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearMeshingElementOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshingElementOptions',)


class GearMeshingElementOptions(_1.APIBase):
    '''GearMeshingElementOptions

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESHING_ELEMENT_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshingElementOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def face_elements(self) -> 'int':
        '''int: 'FaceElements' is the original name of this property.'''

        return self.wrapped.FaceElements

    @face_elements.setter
    def face_elements(self, value: 'int'):
        self.wrapped.FaceElements = int(value) if value else 0

    @property
    def profile_elements(self) -> 'int':
        '''int: 'ProfileElements' is the original name of this property.'''

        return self.wrapped.ProfileElements

    @profile_elements.setter
    def profile_elements(self, value: 'int'):
        self.wrapped.ProfileElements = int(value) if value else 0

    @property
    def fillet_elements(self) -> 'int':
        '''int: 'FilletElements' is the original name of this property.'''

        return self.wrapped.FilletElements

    @fillet_elements.setter
    def fillet_elements(self, value: 'int'):
        self.wrapped.FilletElements = int(value) if value else 0

    @property
    def tip_elements(self) -> 'int':
        '''int: 'TipElements' is the original name of this property.'''

        return self.wrapped.TipElements

    @tip_elements.setter
    def tip_elements(self, value: 'int'):
        self.wrapped.TipElements = int(value) if value else 0

    @property
    def body_elements(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'BodyElements' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.BodyElements) if self.wrapped.BodyElements else None

    @body_elements.setter
    def body_elements(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.BodyElements = value

    @property
    def radial_elements(self) -> 'int':
        '''int: 'RadialElements' is the original name of this property.'''

        return self.wrapped.RadialElements

    @radial_elements.setter
    def radial_elements(self, value: 'int'):
        self.wrapped.RadialElements = int(value) if value else 0

    @property
    def web_elements(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'WebElements' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.WebElements) if self.wrapped.WebElements else None

    @web_elements.setter
    def web_elements(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.WebElements = value

    @property
    def rim_elements(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'RimElements' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.RimElements) if self.wrapped.RimElements else None

    @rim_elements.setter
    def rim_elements(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.RimElements = value
