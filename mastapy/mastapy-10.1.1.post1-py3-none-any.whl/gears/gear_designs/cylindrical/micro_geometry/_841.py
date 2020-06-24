'''_841.py

CylindricalGearFlankMicroGeometry
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import (
    _849, _842, _840, _848,
    _867, _868, _855, _857,
    _863, _865
)
from mastapy.gears.gear_designs.cylindrical import _775
from mastapy.gears.micro_geometry import _355
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearFlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFlankMicroGeometry',)


class CylindricalGearFlankMicroGeometry(_355.FlankMicroGeometry):
    '''CylindricalGearFlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearFlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def read_micro_geometry_from_an_external_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ReadMicroGeometryFromAnExternalFile' is the original name of this property.'''

        return self.wrapped.ReadMicroGeometryFromAnExternalFile

    @read_micro_geometry_from_an_external_file.setter
    def read_micro_geometry_from_an_external_file(self, value: 'Callable[[], None]'):
        value = value if value else None
        self.wrapped.ReadMicroGeometryFromAnExternalFile = value

    @property
    def read_micro_geometry_from_an_external_file_using_file_name(self) -> 'str':
        '''str: 'ReadMicroGeometryFromAnExternalFileUsingFileName' is the original name of this property.'''

        return self.wrapped.ReadMicroGeometryFromAnExternalFileUsingFileName

    @read_micro_geometry_from_an_external_file_using_file_name.setter
    def read_micro_geometry_from_an_external_file_using_file_name(self, value: 'str'):
        self.wrapped.ReadMicroGeometryFromAnExternalFileUsingFileName = str(value) if value else None

    @property
    def modified_normal_pressure_angle_due_to_helix_angle_modification_assuming_unmodified_normal_module_and_pressure_angle_modification(self) -> 'float':
        '''float: 'ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModuleAndPressureAngleModification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModuleAndPressureAngleModification

    @property
    def use_measured_map_data(self) -> 'bool':
        '''bool: 'UseMeasuredMapData' is the original name of this property.'''

        return self.wrapped.UseMeasuredMapData

    @use_measured_map_data.setter
    def use_measured_map_data(self, value: 'bool'):
        self.wrapped.UseMeasuredMapData = bool(value) if value else False

    @property
    def profile_relief(self) -> '_849.CylindricalGearProfileModification':
        '''CylindricalGearProfileModification: 'ProfileRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_849.CylindricalGearProfileModification)(self.wrapped.ProfileRelief) if self.wrapped.ProfileRelief else None

    @property
    def lead_relief(self) -> '_842.CylindricalGearLeadModification':
        '''CylindricalGearLeadModification: 'LeadRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_842.CylindricalGearLeadModification)(self.wrapped.LeadRelief) if self.wrapped.LeadRelief else None

    @property
    def bias(self) -> '_840.CylindricalGearBiasModification':
        '''CylindricalGearBiasModification: 'Bias' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_840.CylindricalGearBiasModification)(self.wrapped.Bias) if self.wrapped.Bias else None

    @property
    def micro_geometry_map(self) -> '_848.CylindricalGearMicroGeometryMap':
        '''CylindricalGearMicroGeometryMap: 'MicroGeometryMap' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_848.CylindricalGearMicroGeometryMap)(self.wrapped.MicroGeometryMap) if self.wrapped.MicroGeometryMap else None

    @property
    def total_lead_relief_points(self) -> 'List[_867.TotalLeadReliefWithDeviation]':
        '''List[TotalLeadReliefWithDeviation]: 'TotalLeadReliefPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TotalLeadReliefPoints, constructor.new(_867.TotalLeadReliefWithDeviation))
        return value

    @property
    def total_profile_relief_points(self) -> 'List[_868.TotalProfileReliefWithDeviation]':
        '''List[TotalProfileReliefWithDeviation]: 'TotalProfileReliefPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TotalProfileReliefPoints, constructor.new(_868.TotalProfileReliefWithDeviation))
        return value

    @property
    def lead_form_deviation_points(self) -> 'List[_855.LeadFormReliefWithDeviation]':
        '''List[LeadFormReliefWithDeviation]: 'LeadFormDeviationPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeadFormDeviationPoints, constructor.new(_855.LeadFormReliefWithDeviation))
        return value

    @property
    def lead_slope_deviation_points(self) -> 'List[_857.LeadSlopeReliefWithDeviation]':
        '''List[LeadSlopeReliefWithDeviation]: 'LeadSlopeDeviationPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeadSlopeDeviationPoints, constructor.new(_857.LeadSlopeReliefWithDeviation))
        return value

    @property
    def profile_form_deviation_points(self) -> 'List[_863.ProfileFormReliefWithDeviation]':
        '''List[ProfileFormReliefWithDeviation]: 'ProfileFormDeviationPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileFormDeviationPoints, constructor.new(_863.ProfileFormReliefWithDeviation))
        return value

    @property
    def profile_slope_deviation_at_10_face_width(self) -> 'List[_865.ProfileSlopeReliefWithDeviation]':
        '''List[ProfileSlopeReliefWithDeviation]: 'ProfileSlopeDeviationAt10FaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileSlopeDeviationAt10FaceWidth, constructor.new(_865.ProfileSlopeReliefWithDeviation))
        return value

    @property
    def profile_slope_deviation_at_50_face_width(self) -> 'List[_865.ProfileSlopeReliefWithDeviation]':
        '''List[ProfileSlopeReliefWithDeviation]: 'ProfileSlopeDeviationAt50FaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileSlopeDeviationAt50FaceWidth, constructor.new(_865.ProfileSlopeReliefWithDeviation))
        return value

    @property
    def profile_slope_deviation_at_90_face_width(self) -> 'List[_865.ProfileSlopeReliefWithDeviation]':
        '''List[ProfileSlopeReliefWithDeviation]: 'ProfileSlopeDeviationAt90FaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileSlopeDeviationAt90FaceWidth, constructor.new(_865.ProfileSlopeReliefWithDeviation))
        return value

    @property
    def gear_design(self) -> '_775.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_775.CylindricalGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    def total_relief(self, face_width: 'float', roll_distance: 'float') -> 'float':
        ''' 'TotalRelief' is the original name of this method.

        Args:
            face_width (float)
            roll_distance (float)

        Returns:
            float
        '''

        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = self.wrapped.TotalRelief(face_width if face_width else 0.0, roll_distance if roll_distance else 0.0)
        return method_result
