'''_764.py

BacklashSpecification
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _794, _792, _819
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_BACKLASH_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'BacklashSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('BacklashSpecification',)


class BacklashSpecification(_819.RelativeValuesSpecification['BacklashSpecification']):
    '''BacklashSpecification

    This is a mastapy class.
    '''

    TYPE = _BACKLASH_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BacklashSpecification.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def normal_backlash(self) -> '_794.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'NormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_794.CylindricalMeshLinearBacklashSpecification)(self.wrapped.NormalBacklash) if self.wrapped.NormalBacklash else None

    @property
    def circumferential_backlash_pitch_circle(self) -> '_794.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'CircumferentialBacklashPitchCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_794.CylindricalMeshLinearBacklashSpecification)(self.wrapped.CircumferentialBacklashPitchCircle) if self.wrapped.CircumferentialBacklashPitchCircle else None

    @property
    def circumferential_backlash_reference_circle(self) -> '_794.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'CircumferentialBacklashReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_794.CylindricalMeshLinearBacklashSpecification)(self.wrapped.CircumferentialBacklashReferenceCircle) if self.wrapped.CircumferentialBacklashReferenceCircle else None

    @property
    def radial_backlash(self) -> '_794.CylindricalMeshLinearBacklashSpecification':
        '''CylindricalMeshLinearBacklashSpecification: 'RadialBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_794.CylindricalMeshLinearBacklashSpecification)(self.wrapped.RadialBacklash) if self.wrapped.RadialBacklash else None

    @property
    def linear_backlash(self) -> 'List[_794.CylindricalMeshLinearBacklashSpecification]':
        '''List[CylindricalMeshLinearBacklashSpecification]: 'LinearBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LinearBacklash, constructor.new(_794.CylindricalMeshLinearBacklashSpecification))
        return value

    @property
    def angular_backlash(self) -> 'List[_792.CylindricalMeshAngularBacklash]':
        '''List[CylindricalMeshAngularBacklash]: 'AngularBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AngularBacklash, constructor.new(_792.CylindricalMeshAngularBacklash))
        return value
