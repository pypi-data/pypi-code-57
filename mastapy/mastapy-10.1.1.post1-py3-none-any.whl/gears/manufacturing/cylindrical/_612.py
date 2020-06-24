'''_612.py

CylindricalGearSpecifiedMicroGeometry
'''


from typing import List

from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _645
from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical import _634, _635
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SPECIFIED_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalGearSpecifiedMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSpecifiedMicroGeometry',)


class CylindricalGearSpecifiedMicroGeometry(_1.APIBase):
    '''CylindricalGearSpecifiedMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SPECIFIED_MICRO_GEOMETRY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSpecifiedMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def lead_measurement_method(self) -> '_645.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'LeadMeasurementMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.LeadMeasurementMethod)
        return constructor.new(_645.MicroGeometryDefinitionMethod)(value) if value else None

    @lead_measurement_method.setter
    def lead_measurement_method(self, value: '_645.MicroGeometryDefinitionMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LeadMeasurementMethod = value

    @property
    def profile_measurement_method(self) -> '_645.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'ProfileMeasurementMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileMeasurementMethod)
        return constructor.new(_645.MicroGeometryDefinitionMethod)(value) if value else None

    @profile_measurement_method.setter
    def profile_measurement_method(self, value: '_645.MicroGeometryDefinitionMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileMeasurementMethod = value

    @property
    def number_of_transverse_planes(self) -> 'int':
        '''int: 'NumberOfTransversePlanes' is the original name of this property.'''

        return self.wrapped.NumberOfTransversePlanes

    @number_of_transverse_planes.setter
    def number_of_transverse_planes(self, value: 'int'):
        self.wrapped.NumberOfTransversePlanes = int(value) if value else 0

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def lead_micro_geometry(self) -> '_634.MicroGeometryInputsLead':
        '''MicroGeometryInputsLead: 'LeadMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_634.MicroGeometryInputsLead)(self.wrapped.LeadMicroGeometry) if self.wrapped.LeadMicroGeometry else None

    @property
    def profile_micro_geometry(self) -> 'List[_635.MicroGeometryInputsProfile]':
        '''List[MicroGeometryInputsProfile]: 'ProfileMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileMicroGeometry, constructor.new(_635.MicroGeometryInputsProfile))
        return value
