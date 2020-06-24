'''_2035.py

BeltCreationOptions
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BELT_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'BeltCreationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltCreationOptions',)


class BeltCreationOptions(_1.APIBase):
    '''BeltCreationOptions

    This is a mastapy class.
    '''

    TYPE = _BELT_CREATION_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltCreationOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.'''

        return self.wrapped.CentreDistance

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value else 0.0

    @property
    def pulley_a_diameter(self) -> 'float':
        '''float: 'PulleyADiameter' is the original name of this property.'''

        return self.wrapped.PulleyADiameter

    @pulley_a_diameter.setter
    def pulley_a_diameter(self, value: 'float'):
        self.wrapped.PulleyADiameter = float(value) if value else 0.0

    @property
    def pulley_b_diameter(self) -> 'float':
        '''float: 'PulleyBDiameter' is the original name of this property.'''

        return self.wrapped.PulleyBDiameter

    @pulley_b_diameter.setter
    def pulley_b_diameter(self, value: 'float'):
        self.wrapped.PulleyBDiameter = float(value) if value else 0.0

    @property
    def speed_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpeedRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpeedRatio) if self.wrapped.SpeedRatio else None

    @speed_ratio.setter
    def speed_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpeedRatio = value
