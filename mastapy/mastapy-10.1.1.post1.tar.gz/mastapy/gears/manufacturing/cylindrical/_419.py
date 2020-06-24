'''_419.py

MicroGeometryInputsProfile
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical import _417, _421
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_INPUTS_PROFILE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'MicroGeometryInputsProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryInputsProfile',)


class MicroGeometryInputsProfile(_417.MicroGeometryInputs['_421.ProfileModificationSegment']):
    '''MicroGeometryInputsProfile

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_INPUTS_PROFILE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryInputsProfile.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def z_plane(self) -> 'float':
        '''float: 'ZPlane' is the original name of this property.'''

        return self.wrapped.ZPlane

    @z_plane.setter
    def z_plane(self, value: 'float'):
        self.wrapped.ZPlane = float(value) if value else 0.0

    @property
    def number_of_profile_segments(self) -> 'int':
        '''int: 'NumberOfProfileSegments' is the original name of this property.'''

        return self.wrapped.NumberOfProfileSegments

    @number_of_profile_segments.setter
    def number_of_profile_segments(self, value: 'int'):
        self.wrapped.NumberOfProfileSegments = int(value) if value else 0
